import asyncio
import random
from faker import Faker
from app.db.database import connect_db, disconnect_db, execute, fetchrow, fetch
from app.core.security import hash_password

fake = Faker("fa_IR")

NUM_USERS = 1000
NUM_OPERATORS = 50
NUM_BUSES = 100
NUM_TRIPS = 1200
TARGET_BOOKINGS = 100000

provinces_data = {
    "تهران": ["تهران", "ری", "شمیرانات"],
    "اصفهان": ["اصفهان", "کاشان", "نجف‌آباد"],
    "فارس": ["شیراز", "مرودشت", "کازرون"],
    "مشهد": ["مشهد", "نیشابور", "تربت جام"],
    "قم": ["قم", "دلیجان"],
    "مازندران": ["ساری", "بابل", "قائم‌شهر"]
}

async def seed_provinces_and_cities():
    province_map = {}
    for prov, cities in provinces_data.items():
        res = await fetchrow("INSERT INTO provinces(province_name) VALUES($1) RETURNING id", prov)
        province_map[prov] = res["id"]
        for city in cities:
            await execute("INSERT INTO cities(city_name, province_id) VALUES($1,$2)", city, res["id"])
    return province_map

async def seed_users_and_wallets():
    users = []
    hashed = hash_password("000123")
    for i in range(NUM_USERS):
        full_name = fake.name()
        phone = fake.unique.numerify("09#########")
        is_admin = True if i < NUM_OPERATORS else False
        user = await fetchrow(
            "INSERT INTO users(full_name, phone_number, hashed_password, is_active, is_admin) VALUES($1,$2,$3,true,$4) RETURNING id",
            full_name, phone, hashed, is_admin
        )
        await execute("INSERT INTO wallets(user_id, balance) VALUES($1,$2)", user["id"], random.randint(100000,500000))
        users.append(user["id"])
    return users

async def seed_operators(users):
    ops = []
    for user_id in users[:NUM_OPERATORS]:
        company_name = fake.company()
        license_number = fake.unique.bothify("??####")
        await execute("INSERT INTO operators(user_id, company_name, license_number) VALUES($1,$2,$3)", user_id, company_name, license_number)
        ops.append(user_id)
    return ops

async def seed_buses(operators):
    buses = []
    for _ in range(NUM_BUSES):
        op_id = random.choice(operators)
        plate = fake.unique.bothify("??####??")
        capacity = random.randint(100, 120)
        bus = await fetchrow("INSERT INTO buses(operator_id, plate_number, capacity) VALUES($1,$2,$3) RETURNING id", op_id, plate, capacity)
        buses.append({"id": bus["id"], "capacity": capacity})
    return buses

async def seed_trips(buses):
    trips = []
    for _ in range(NUM_TRIPS):
        bus = random.choice(buses)
        dep_time = fake.future_datetime(end_date="+30d")
        arr_time = dep_time + fake.time_delta(end_datetime=dep_time)
        price = random.randint(50000, 500000)
        trip = await fetchrow("INSERT INTO trips(bus_id, departure_time, arrival_time, price, status) VALUES($1,$2,$3,$4,'scheduled') RETURNING id", bus["id"], dep_time, arr_time, price)
        # ایجاد صندلی‌ها
        for seat_num in range(1, bus["capacity"]+1):
            await execute("INSERT INTO seats(trip_id, seat_number, status) VALUES($1,$2,'available')", trip["id"], seat_num)
        trips.append(trip["id"])
    return trips

from app.models.booking_model import BookingStatus, PaymentStatus
from app.models.transaction_model import TransactionType, PaymentMethod, TransactionStatus
import random
from app.db.database import fetch, fetchrow, execute

async def seed_bookings(users, trips, TARGET_BOOKINGS=100000):
    bookings_created = 0

    while bookings_created < TARGET_BOOKINGS:
        user_id = random.choice(users)
        trip_id = random.choice(trips)

        # گرفتن صندلی‌های آزاد
        seats = await fetch("SELECT id FROM seats WHERE trip_id=$1 AND status='available'", trip_id)
        if not seats:
            continue

        seat = random.choice(seats)

        # رزرو صندلی
        await execute("UPDATE seats SET status='reserved' WHERE id=$1", seat["id"])

        # ایجاد Booking
        booking = await fetchrow(
            "INSERT INTO bookings(user_id, trip_id, seat_id, status, payment_status) "
            "VALUES($1,$2,$3,$4,$5) RETURNING id",
            user_id, trip_id, seat["id"], BookingStatus.confirmed.value, PaymentStatus.paid.value
        )

        # ایجاد Transaction
        await execute(
            "INSERT INTO transactions(user_id, related_booking_id, amount, type, method, status, wallet_balance_after) "
            "VALUES($1,$2,$3,$4,$5,$6,(SELECT balance FROM wallets WHERE user_id=$1))",
            user_id, booking["id"], random.randint(50000, 500000),
            TransactionType.debit.value, PaymentMethod.wallet.value, TransactionStatus.completed.value
        )

        bookings_created += 1
        if bookings_created % 1000 == 0:
            print(f"{bookings_created} bookings created...")


async def main():
    await connect_db()
    await seed_provinces_and_cities()
    users = await seed_users_and_wallets()
    operators = await seed_operators(users)
    buses = await seed_buses(operators)
    trips = await seed_trips(buses)
    await seed_bookings(users, trips)
    await disconnect_db()

if __name__ == "__main__":
    asyncio.run(main())
