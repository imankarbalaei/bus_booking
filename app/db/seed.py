import asyncio
import random
from faker import Faker
from app.db.database import connect_db, disconnect_db, pool, get_pool
from app.core.security import hash_password
from app.models.booking_model import BookingStatus, PaymentStatus

fake = Faker("fa_IR")

NUM_USERS = 1000
NUM_OPERATORS = 50
NUM_BUSES = 100
NUM_TRIPS = 1200
NUM_ROUTES = 100
TARGET_BOOKINGS = 100_000
BATCH_SIZE = 5000

provinces_data = {
    "تهران": ["تهران", "ری", "شمیرانات"],
    "اصفهان": ["اصفهان", "کاشان", "نجف‌آباد"],
    "فارس": ["شیراز", "مرودشت", "کازرون"],
    "خراسان رضوی": ["مشهد", "نیشابور", "تربت جام"],
    "قم": ["قم", "دلیجان"],
    "مازندران": ["ساری", "بابل", "قائم‌شهر"]
}


async def seed_provinces_and_cities():
    province_map = {}
    province_values = [(prov,) for prov in provinces_data]
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        await conn.copy_records_to_table("provinces", records=province_values, columns=["province_name"])
        rows = await conn.fetch("SELECT id, province_name FROM provinces")
        for row in rows:
            province_map[row["province_name"]] = row["id"]
            city_values = [(city, row["id"]) for city in provinces_data[row["province_name"]]]
            await conn.copy_records_to_table("cities", records=city_values, columns=["city_name","province_id"])
    return province_map


async def seed_routes():
    route_values = []
    for _ in range(NUM_ROUTES):
        origin = random.randint(1, 17)
        dest = random.randint(1, 17)
        while dest == origin:
            dest = random.randint(1, 17)
        distance = random.randint(50, 1000)
        route_values.append((origin, dest, distance))
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        await conn.copy_records_to_table("routes", records=route_values,
                                         columns=["origin_city_id","destination_city_id","distance_km"])
        rows = await conn.fetch("SELECT id FROM routes")
    return [r["id"] for r in rows]


async def seed_users_and_wallets():
    hashed = hash_password("000123")
    user_values = [(fake.name(), fake.unique.numerify("09#########"), hashed, True, i < NUM_OPERATORS)
                   for i in range(NUM_USERS)]
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        await conn.copy_records_to_table("users", records=user_values,
                                         columns=["full_name","phone_number","hashed_password","is_active","is_admin"])
        users = await conn.fetch("SELECT id FROM users")
        wallet_values = [(u["id"], random.randint(100_000, 500_000)) for u in users]
        await conn.copy_records_to_table("wallets", records=wallet_values, columns=["user_id","balance"])

    admin_hashed = hash_password("12345678")
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        admin = await conn.fetchrow(
            "INSERT INTO users(full_name, phone_number, email, hashed_password, is_active, is_admin) "
            "VALUES($1,$2,$3,$4,true,true) RETURNING id",
            "Iman", "09121112211", "iman@example.com", admin_hashed
        )
        await conn.execute("INSERT INTO wallets(user_id, balance) VALUES($1,$2)", admin["id"], 100_000)
    return [u["id"] for u in users] + [admin["id"]]


async def seed_operators(users):
    operator_values = [(user_id, fake.company(), fake.unique.bothify("??####")) for user_id in users[:NUM_OPERATORS]]
      # استفاده از connection برای copy
    conn_pool = await get_pool()
    await conn_pool.acquire().__aenter__()
    async with conn_pool.acquire() as conn:
        await conn.copy_records_to_table("operators", records=operator_values,
                                         columns=["user_id","company_name","license_number"])
    return [u[0] for u in operator_values]


async def seed_buses(operators, routes):
    bus_values = [(random.choice(operators), fake.unique.bothify("??####??"), random.randint(100,120), random.choice(routes))
                  for _ in range(NUM_BUSES)]
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        await conn.copy_records_to_table("buses", records=bus_values,
                                         columns=["operator_id","plate_number","capacity","route_id"])
        rows = await conn.fetch("SELECT id, capacity FROM buses")
    return rows


async def seed_trips(buses):
    trip_values = []
    seat_values = []
    for _ in range(NUM_TRIPS):
        bus = random.choice(buses)
        dep_time = fake.future_datetime(end_date="+30d")
        arr_time = dep_time + fake.time_delta(end_datetime=dep_time)
        price = random.randint(50_000, 500_000)
        trip_values.append((bus["id"], dep_time, arr_time, price, 'scheduled', bus["capacity"]))
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        await conn.copy_records_to_table("trips", records=[t[:5] for t in trip_values],
                                         columns=["bus_id","departure_time","arrival_time","price","status"])
        trips = await conn.fetch("SELECT id, bus_id FROM trips")

        for trip, (_, _, _, _, _, capacity) in zip(trips, trip_values):
            seat_values.extend([(trip["id"], i+1, 'available') for i in range(capacity)])
        await conn.copy_records_to_table("seats", records=seat_values, columns=["trip_id","seat_number","status"])
    return trips


async def seed_bookings(users, trips, TARGET_BOOKINGS=100_000):
    trip_seats_map = {}
    conn_pool = await get_pool()
    async with conn_pool.acquire() as conn:
        seats = await conn.fetch("SELECT id, trip_id FROM seats WHERE status='available'")
        for seat in seats:
            trip_seats_map.setdefault(seat["trip_id"], []).append(seat["id"])

    bookings_created = 0
    batch = []
    seat_updates = []
    while bookings_created < TARGET_BOOKINGS:
        user_id = random.choice(users)
        trip_id = random.choice(list(trip_seats_map.keys()))
        if not trip_seats_map[trip_id]:
            continue
        seat_id = trip_seats_map[trip_id].pop()
        batch.append((user_id, trip_id, seat_id, BookingStatus.confirmed.value, PaymentStatus.paid.value))
        seat_updates.append(seat_id)
        bookings_created += 1

        if len(batch) >= BATCH_SIZE:
            conn_pool = await get_pool()
            async with conn_pool.acquire() as conn:
                await conn.copy_records_to_table("bookings", records=batch,
                                                 columns=["user_id","trip_id","seat_id","status","payment_status"])
                await conn.execute("UPDATE seats SET status='reserved' WHERE id = ANY($1)", seat_updates)
            batch.clear()
            seat_updates.clear()
            print(f"{bookings_created} bookings created...")


    if batch:
        conn_pool = await get_pool()
        async with conn_pool.acquire() as conn:
            await conn.copy_records_to_table("bookings", records=batch,
                                             columns=["user_id","trip_id","seat_id","status","payment_status"])
            await conn.execute("UPDATE seats SET status='reserved' WHERE id = ANY($1)", seat_updates)
    print("✅ Booking seeding completed.")


async def main():
    await connect_db()
    await seed_provinces_and_cities()
    routes = await seed_routes()
    users = await seed_users_and_wallets()
    operators = await seed_operators(users)
    buses = await seed_buses(operators, routes)
    trips = await seed_trips(buses)
    await seed_bookings(users, trips)
    await disconnect_db()

if __name__ == "__main__":
    asyncio.run(main())
