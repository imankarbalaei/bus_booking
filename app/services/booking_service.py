# app/services/booking_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import selectinload

from app.models.booking_model import BookingStatus, PaymentStatus
from app.models.trip_model import Trip
from app.models.wallet_model import Wallet
from app.crud.booking_crud import BookingCRUD
from app.schemas.booking_schema import PaymentMethod


class BookingService:
    @staticmethod
    async def reserve_seat(session: AsyncSession, user, trip_id: int, payment_method: PaymentMethod):
        # تمام عملیات داخل یک transaction امن
        async with session.begin():
            # 1️⃣ دریافت سفر و lock کردن row برای جلوگیری از overbooking
            result = await session.execute(
                select(Trip)
                .options(selectinload(Trip.bus))  # اضافه شد
                .where(Trip.id == trip_id)
                .with_for_update()
            )
            trip = result.scalar_one_or_none()
            if not trip:
                raise HTTPException(status_code=404, detail="Trip not found")

            # 2️⃣ بررسی ظرفیت
            bookings = await BookingCRUD.get_bookings_by_trip(session, trip_id)
            if len(bookings) >= trip.bus.capacity:
                raise HTTPException(status_code=400, detail="No available seats")

            # 3️⃣ محدودیت روزانه کاربر
            today = datetime.utcnow().date()
            count = await BookingCRUD.get_user_bookings_count(session, user.id, today)
            if count >= 20:
                raise HTTPException(status_code=400, detail="Daily booking limit reached")

            amount = trip.price

            # 4️⃣ پرداخت با Wallet
            if payment_method == PaymentMethod.wallet:
                wallet = await session.get(Wallet, user.id)
                if not wallet or wallet.price < amount:
                    raise HTTPException(status_code=400, detail="Insufficient wallet balance")

                wallet.price -= amount

                booking = await BookingCRUD.create_booking(session, user.id, trip_id, amount)
                transaction = await BookingCRUD.create_transaction(
                    session, user.id, booking.id, amount, PaymentMethod.wallet, wallet_id=wallet.id,wallet_balance_after=wallet.price
                )
                transaction.wallet_balance_after = wallet.price
                return booking

            # 5️⃣ پرداخت با Gateway
            elif payment_method == PaymentMethod.gateway:
                booking = await BookingCRUD.create_booking(session, user.id, trip_id, amount)
                transaction = await BookingCRUD.create_transaction(
                    session, user.id, booking.id, amount, PaymentMethod.gateway,
                )
                # TODO: اتصال به درگاه پرداخت
                return booking

    @staticmethod
    async def cancel_booking(session:AsyncSession, user, booking_id: int):
        async with session.begin():
            booking = await BookingCRUD.get_booking_by_id(session, booking_id)
            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found")

            # فقط صاحب رزرو حق لغو دارد
            if booking.user_id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to cancel this booking")

            # فقط رزرو فعال و پرداخت شده قابل لغو است
            if booking.status != BookingStatus.booked or booking.payment_status != PaymentStatus.paid:
                raise HTTPException(status_code=400, detail="Booking cannot be canceled")

            # کیف پول کاربر
            wallet = await session.execute(
                select(Wallet).where(Wallet.user_id == user.id).with_for_update()
            )
            wallet = wallet.scalar_one_or_none()
            if not wallet:
                raise HTTPException(status_code=404, detail="Wallet not found")

            # بازگشت مبلغ
            refund_amount = booking.trip.price
            wallet.price += refund_amount

            # بروزرسانی وضعیت رزرو
            await BookingCRUD.cancel_booking(session, booking)

            # ثبت تراکنش برگشتی
            transaction = await BookingCRUD.create_refund_transaction(
                session,
                user.id,
                booking.id,
                refund_amount,
                wallet_id=wallet.id
            )
            transaction.wallet_balance_after = wallet.price

            return {
                "id": booking.id,
                "trip_id": booking.trip_id,
                "status": booking.status.value,
                "payment_status": booking.payment_status.value,
                "refund_amount": refund_amount
            }




