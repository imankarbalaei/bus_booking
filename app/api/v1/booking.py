from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session
from app.schemas.booking_schema import BookingCreate, BookingResponse
from app.services.booking_service import BookingService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/bookings", tags=["Booking"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def reserve_trip(booking_in: BookingCreate, user = Depends(get_current_user)):
    async with async_session() as session:
        async with session.begin():
            booking = await BookingService.reserve_seat(session, user, booking_in.trip_id)
            return booking
