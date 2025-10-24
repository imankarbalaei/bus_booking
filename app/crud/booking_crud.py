from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.booking_model import Booking, BookingStatus
from app.models.trip_model import Trip

class BookingCRUD:
    @staticmethod
    async def get_bookings_by_trip(session: AsyncSession, trip_id: int):
        result = await session.execute(select(Booking).where(Booking.trip_id == trip_id))
        return result.scalars().all()

    @staticmethod
    async def get_user_bookings_count(session: AsyncSession, user_id: int, date):
        # تعداد رزرو کاربر در یک روز
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        result = await session.execute(
            select(func.count(Booking.id))
            .where(Booking.user_id == user_id)
            .where(Booking.booking_time.between(start, end))
        )
        return result.scalar()

    @staticmethod
    async def create_booking(session: AsyncSession, user_id: int, trip_id: int):
        booking = Booking(
            user_id=user_id,
            trip_id=trip_id,
            status=BookingStatus.booked,
            payment_status="paid"
        )
        session.add(booking)
        await session.flush()
        return booking
