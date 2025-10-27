# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.database import get_session
# from app.models.user_model import User
# from core.dependencies import get_current_admin
# from app.repositories.admin_crud import create_bus, create_trip
# from app.schemas.admin_schema import BusCreate, BusResponse, TripCreate, TripResponse
#
# router = APIRouter(prefix="/admin", tags=["Admin"])
#
#
# @router.post("/buses/add", response_model=BusResponse)
# async def admin_create_bus(
#     bus_in: BusCreate,
#     session: AsyncSession = Depends(get_session),
#     admin: User = Depends(get_current_admin)
# ):
#     """
#     🚌 ایجاد اتوبوس جدید (فقط برای ادمین)
#     """
#     bus = await create_bus(session, bus_in.plate_number, bus_in.capacity, bus_in.route_id, bus_in.operator_id)
#     return bus
#
#
# @router.post("/trips/add", response_model=TripResponse)
# async def admin_create_trip(
#     trip_in: TripCreate,
#     session: AsyncSession = Depends(get_session),
#     admin: User = Depends(get_current_admin)
# ):
#     """
#     🚍 ایجاد سفر جدید (فقط برای ادمین)
#     """
#     trip = await create_trip(
#         session,
#         trip_in.bus_id,
#         trip_in.departure_time,
#         trip_in.arrival_time,
#         trip_in.price
#     )
#     return trip
