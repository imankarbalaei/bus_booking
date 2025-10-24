# app/crud/booking_crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.booking_model import Booking, BookingStatus, PaymentStatus
from app.models.transaction_model import Transaction, TransactionType, TransactionStatus
from app.schemas.booking_schema import PaymentMethod


class BookingCRUD:
    @staticmethod
    async def get_bookings_by_trip(session: AsyncSession, trip_id: int):
        result = await session.execute(select(Booking).where(Booking.trip_id == trip_id
                                                             , Booking.status == BookingStatus.booked,
                                                             Booking.payment_status == PaymentStatus.paid))
        return result.scalars().all()

    @staticmethod
    async def get_user_bookings_count(session: AsyncSession, user_id: int, date):
        result = await session.execute(
            select(func.count(Booking.id))
            .where(Booking.user_id == user_id)
            .where(func.date(Booking.booking_time) == date)
        )
        return result.scalar() or 0

    @staticmethod
    async def create_booking(session: AsyncSession, user_id: int, trip_id: int, amount: int):
        booking = Booking(
            user_id=user_id,
            trip_id=trip_id,
            status="booked",
            payment_status="paid"
        )
        session.add(booking)
        await session.flush()  # اطمینان از ایجاد id قبل از استفاده در transaction
        return booking

    @staticmethod
    async def create_transaction(session: AsyncSession, user_id: int, booking_id: int, amount: int,
                                 method: PaymentMethod, wallet_id: int | None = None,
                                 wallet_balance_after: int | None = None):
        status = TransactionStatus.success if method == PaymentMethod.wallet else TransactionStatus.pending
        transaction = Transaction(
            user_id=user_id,
            wallet_id=wallet_id,
            related_booking_id=booking_id,
            amount=amount,
            type=TransactionType.direct_payment,
            method=method,
            status=status,
            wallet_balance_after=wallet_balance_after or 0
        )
        session.add(transaction)
        await session.flush()
        return transaction


    @staticmethod
    async def get_booking_by_id(session: AsyncSession, booking_id: int):
        result = await session.execute(select(Booking).options(selectinload(Booking.trip)).where(Booking.id == booking_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def cancel_booking(session: AsyncSession, booking: Booking):
        booking.status = BookingStatus.canceled
        booking.payment_status = PaymentStatus.refunded
        await session.flush()
        return booking

    @staticmethod
    async def create_refund_transaction(session: AsyncSession, user_id: int, booking_id: int, amount: int, wallet_id: int):
        transaction = Transaction(
            user_id=user_id,
            wallet_id=wallet_id,
            related_booking_id=booking_id,
            amount=amount,
            type=TransactionType.refund,
            method=PaymentMethod.wallet,
            status=TransactionStatus.success,
            wallet_balance_after=0
        )
        session.add(transaction)
        await session.flush()
        return transaction
