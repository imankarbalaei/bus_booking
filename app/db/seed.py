import asyncio
import random
from faker import Faker
from sqlalchemy import select
from app.db.database import async_session
from app.models.city_model import Province, City
from app.models.route_model import Route
from app.models.user_model import User
from app.models.operator_model import Operator
from app.models.wallet_model import Wallet
from app.models.transaction_model import Transaction
from app.models.bus_model import Bus
from app.models.trip_model import Trip
from app.models.booking_model import Booking
from app.core.security import hash_password

fake = Faker()


# --------------------------
# 1️⃣ Provinces & Cities
# --------------------------
async def seed_provinces_and_cities():
    data = {
        "تهران": ["تهران", "ری", "شمیرانات"],
        "اصفهان": ["اصفهان", "کاشان", "نجف‌آباد"],
        "فارس": ["شیراز", "مرودشت", "کازرون"],
        "مشهد": ["مشهد", "نیشابور", "تربت جام"],
        "قم": ["قم", "دلیجان"],
        "مازندران": ["ساری", "بابل", "قائم‌شهر"]
    }
    async with async_session() as session:
        async with session.begin():
            for province_name, cities in data.items():
                province = Province(province_name=province_name)
                session.add(province)
                await session.flush()
                for city_name in cities:
                    city = City(city_name=city_name, province_id=province.id)
                    session.add(city)
        print("Seeded provinces and cities")


# --------------------------
# 2️⃣ Routes (حداقل 20)
# --------------------------
routes_data = [
    ("تهران", "اصفهان", 450),
    ("تهران", "شیراز", 900),
    ("تهران", "مشهد", 900),
    ("تهران", "قم", 150),
    ("تهران", "ساری", 250),
    ("اصفهان", "تهران", 450),
    ("اصفهان", "شیراز", 400),
    ("اصفهان", "مشهد", 850),
    ("اصفهان", "قم", 300),
    ("اصفهان", "ساری", 550),
    ("شیراز", "تهران", 900),
    ("شیراز", "اصفهان", 400),
    ("شیراز", "مشهد", 950),
    ("شیراز", "قم", 900),
    ("شیراز", "ساری", 1200),
    ("مشهد", "تهران", 900),
    ("مشهد", "اصفهان", 850),
    ("مشهد", "شیراز", 950),
    ("قم", "تهران", 150),
    ("ساری", "بابل", 50)
]


async def seed_routes():
    async with async_session() as session:
        async with session.begin():
            cities_result = await session.execute(select(City))
            cities_list = cities_result.scalars().all()
            for origin_name, dest_name, distance in routes_data:
                origin_city = next(c for c in cities_list if c.city_name == origin_name)
                dest_city = next(c for c in cities_list if c.city_name == dest_name)
                route = Route(
                    origin_city_id=origin_city.id,
                    destination_city_id=dest_city.id,
                    distance_km=distance
                )
                session.add(route)
        print("Seeded 20 routes")


# --------------------------
# 3️⃣ Users
# --------------------------
async def seed_users(n=1000):
    async with async_session() as session:
        async with session.begin():
            for _ in range(n):
                phone_number = "09" + "".join([str(random.randint(0, 9)) for _ in range(9)])
                user = User(
                    full_name=fake.name()[:50],
                    phone_number=phone_number,
                    email=fake.unique.email()[:50],
                    hashed_password=hash_password("00123")
                )
                session.add(user)
        print(f"Seeded {n} users")


# --------------------------
# 4️⃣ Operators
# --------------------------
async def seed_operators(n=50):
    async with async_session() as session:
        async with session.begin():
            for i in range(1, n + 1):
                operator = Operator(
                    user_id=i,
                    company_name=fake.company()[:20],
                    license_number=fake.unique.bothify(text='???-#####')
                )
                session.add(operator)
        print(f"Seeded {n} operators")


# --------------------------
# 5️⃣ Wallets + Transactions
# --------------------------
async def seed_wallets():
    async with async_session() as session:
        async with session.begin():
            for user_id in range(1, 1001):
                amount = random.randint(1000, 10000)
                wallet = Wallet(
                    user_id=user_id,
                    price=amount
                )
                session.add(wallet)
                await session.flush()
                transaction = Transaction(
                    user_id=user_id,
                    wallet_id=wallet.id,
                    amount=amount,
                    type="topup",
                    method="manual",
                    status="success",
                    wallet_balance_after=amount
                )
                session.add(transaction)
        print("Seeded wallets with initial transactions")


# --------------------------
# 6️⃣ Buses
# --------------------------
async def seed_buses(n=50):
    async with async_session() as session:
        async with session.begin():
            routes_result = await session.execute(select(Route.id))
            route_ids = [r[0] for r in routes_result.all()]
            for _ in range(n):
                bus = Bus(
                    plate_number=fake.unique.bothify(text='##?#####'),
                    capacity=random.randint(30, 60),
                    operator_id=random.randint(1, 50),
                    route_id=random.choice(route_ids)
                )
                session.add(bus)
        print(f"Seeded {n} buses")


# --------------------------
# 7️⃣ Trips
# --------------------------
async def seed_trips(n=500):
    async with async_session() as session:
        async with session.begin():
            buses_result = await session.execute(select(Bus.id))
            bus_ids = [b[0] for b in buses_result.all()]
            for _ in range(n):
                trip = Trip(
                    bus_id=random.choice(bus_ids),
                    departure_time=fake.date_time_this_month(),
                    arrival_time=fake.date_time_this_month(),
                    price=random.randint(100, 500)
                )
                session.add(trip)
        print(f"Seeded {n} trips")


# --------------------------
# 8️⃣ Bookings + Transactions (Batch-wise)
# --------------------------
BATCH_SIZE = 1000


async def seed_bookings(n=100_000):
    trips_result = None
    async with async_session() as session:
        trips_result = await session.execute(select(Trip.id))
        trip_ids = [t[0] for t in trips_result.all()]

    for start in range(0, n, BATCH_SIZE):
        end = min(start + BATCH_SIZE, n)
        async with async_session() as session:
            async with session.begin():
                for _ in range(start, end):
                    user_id = random.randint(1, 1000)
                    trip_id = random.choice(trip_ids)
                    booking = Booking(
                        user_id=user_id,
                        trip_id=trip_id,
                        status="booked",
                        payment_status="paid"
                    )
                    session.add(booking)

                await session.flush()


                for booking in session.new:
                    transaction = Transaction(
                        user_id=booking.user_id,
                        related_booking_id=booking.id,
                        wallet_id=None,
                        amount=random.randint(100, 500),
                        type="direct_payment",
                        method="manual",
                        status="success",
                        wallet_balance_after=0
                    )
                    session.add(transaction)
            print(f"Inserted bookings: {end}/{n}")

    print(f"Seeded {n} bookings with transactions")



# --------------------------
# Seed All
# --------------------------
async def seed_all():
    print("Seeding Provinces & Cities...")
    await seed_provinces_and_cities()

    print("Seeding Routes...")
    await seed_routes()

    print("Seeding Users...")
    await seed_users()

    print("Seeding Operators...")
    await seed_operators()

    print("Seeding Wallets + initial transactions...")
    await seed_wallets()

    print("Seeding Buses...")
    await seed_buses()

    print("Seeding Trips...")
    await seed_trips()

    print("Seeding Bookings + Transactions (100k)...")
    await seed_bookings()


if __name__ == "__main__":
    asyncio.run(seed_all())



