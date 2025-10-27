# from sqlalchemy import select
# from app.models.bus_model import Bus
# from app.models.trip_model import Trip
# from datetime import datetime
# from fastapi import HTTPException
#
#
# async def create_bus(session, plate_number: str, capacity: int, route_id: int,operator_id: int):
#     # چک تکراری نبودن پلاک
#     existing = await session.execute(select(Bus).where(Bus.plate_number == plate_number))
#     if existing.scalar_one_or_none():
#         raise HTTPException(status_code=400, detail="Bus with this plate number already exists")
#
#     bus = Bus(plate_number=plate_number, capacity=capacity, route_id=route_id, operator_id=operator_id)
#     session.add(bus)
#     await session.commit()
#     await session.refresh(bus)
#     return bus
#
#
#
# async def create_trip(session, bus_id: int, departure_time: datetime, arrival_time: datetime, price: int):
#     # 1️⃣ بررسی زمان‌ها
#     now = datetime.now(departure_time.tzinfo)
#     if departure_time < now:
#         raise HTTPException(status_code=400, detail="Departure time cannot be in the past")
#     if arrival_time <= departure_time:
#         raise HTTPException(status_code=400, detail="Arrival time must be after departure time")
#
#     # 2️⃣ بررسی وجود اتوبوس
#     bus_result = await session.execute(select(Bus).where(Bus.id == bus_id))
#     bus = bus_result.scalar_one_or_none()
#     if not bus:
#         raise HTTPException(status_code=404, detail="Bus not found")
#
#     # 3️⃣ بررسی اینکه اتوبوس قبلاً در آن زمان سفری ندارد
#     overlap_stmt = select(Trip).where(
#         (Trip.bus_id == bus_id) &
#         (
#             ((Trip.departure_time <= departure_time) & (Trip.arrival_time > departure_time)) |
#             ((Trip.departure_time < arrival_time) & (Trip.arrival_time >= arrival_time))
#         )
#     )
#     overlapping = await session.execute(overlap_stmt)
#     if overlapping.scalar_one_or_none():
#         raise HTTPException(status_code=400, detail="Bus already has a trip during this time range")
#
#     # 4️⃣ ایجاد سفر
#     trip = Trip(
#         bus_id=bus_id,
#         departure_time=departure_time,
#         arrival_time=arrival_time,
#         price=price,
#     )
#     session.add(trip)
#     await session.commit()
#     await session.refresh(trip)
#     return trip
