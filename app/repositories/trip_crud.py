# # app/repositories/trip_crud.py
# from sqlalchemy import select, func, asc, desc
# from sqlalchemy.orm import selectinload
# from app.models.trip_model import Trip
# from app.models.booking_model import Booking, BookingStatus
# from app.models.bus_model import Bus
# from app.models.route_model import Route
# from app.models.city_model import City
#
# async def get_available_trips(session, origin: str = None, destination: str = None, order_by: str = "asc"):
#     # query اصلی
#     stmt = (
#         select(Trip)
#         .join(Bus, Trip.bus_id == Bus.id)
#         .join(Route, Bus.route_id == Route.id)
#         .options(
#             selectinload(Trip.bus)
#             .selectinload(Bus.route)
#             .selectinload(Route.origin_city),
#             selectinload(Trip.bus)
#             .selectinload(Bus.route)
#             .selectinload(Route.destination_city),
#             selectinload(Trip.bookings)
#         )
#     )
#
#     # فیلتر مبدا و مقصد
#     if origin:
#         stmt = stmt.where(Route.origin_city.has(City.city_name == origin))
#     if destination:
#         stmt = stmt.where(Route.destination_city.has(City.city_name == destination))
#
#     # اجرای query
#     result = await session.execute(stmt)
#     trips = result.scalars().all()
#
#     available_trips = []
#     for trip in trips:
#         # محاسبه صندلی آزاد
#         booked_count = sum(1 for b in trip.bookings if b.status == BookingStatus.booked)
#         available_seats = trip.bus.capacity - booked_count
#         if available_seats > 0:
#             trip.available_seats = available_seats
#             trip.origin = trip.bus.route.origin_city.city_name
#             trip.destination = trip.bus.route.destination_city.city_name
#             available_trips.append(trip)
#
#     # مرتب‌سازی بر اساس قیمت
#     reverse = order_by == "desc"
#     available_trips.sort(key=lambda x: x.price, reverse=reverse)
#
#     return available_trips
