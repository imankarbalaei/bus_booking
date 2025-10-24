from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.booking_crud import BookingCRUD
from app.models.trip_model import Trip
from fastapi import HTTPException, status

class BookingService:
    @staticmethod
    async def reserve_seat(session: AsyncSession, user, trip_id: int):

        trip = await session.get(Trip, trip_id)
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")

        bookings = await BookingCRUD.get_bookings_by_trip(session, trip_id)
        if len(bookings) >= trip.bus.capacity:
            raise HTTPException(status_code=400, detail="No available seats")

        today = datetime.utcnow().date()
        count = await BookingCRUD.get_user_bookings_count(session, user.id, today)
        if count >= 20:
            raise HTTPException(status_code=400, detail="Daily booking limit reached")

        booking = await BookingCRUD.create_booking(session, user.id, trip_id)
        return booking
