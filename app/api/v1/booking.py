from fastapi import APIRouter, Depends, status
from app.db.database import get_session
from app.schemas.booking_schema import BookingCreate, BookingCancelResponse
from app.services.booking_service import BookingService
from app.api.dependencies import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

router = APIRouter(prefix="/bookings", tags=["Booking"])



@router.post("/")
async def reserve_trip(
    booking_in: BookingCreate,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    booking = await BookingService.reserve_seat(session, user, booking_in.trip_id, booking_in.payment_method)
    return booking

@router.post("/{booking_id}/cancel", response_model=BookingCancelResponse, status_code=status.HTTP_200_OK)
async def cancel_booking(
    booking_id: int,
    user = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    result = await BookingService.cancel_booking(session, user, booking_id)
    return result


