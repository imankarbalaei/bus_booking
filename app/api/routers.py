from fastapi import APIRouter

from app.api.v1 import auth_router, booking_router,trips_router,admin_router

api_router = APIRouter()
api_router.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
api_router.include_router(booking_router.router, prefix="/bookings", tags=["Bookings"])
api_router.include_router(trips_router.router, prefix="/trips", tags=["Trips"])
api_router.include_router(admin_router.router, prefix="/admin", tags=["Admin"])
