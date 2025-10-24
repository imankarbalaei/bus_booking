from fastapi import APIRouter
from app.api.v1 import auth,booking

API_VERSION_PREFIX = '/v1'
api_router = APIRouter(prefix=f"{API_VERSION_PREFIX}")

api_router.include_router(booking.router)
api_router.include_router(auth.router)

