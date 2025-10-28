from fastapi import HTTPException
from typing import List
from app.repositories.booking_repo import BookingRepo
from app.db.database import get_pool
import datetime
from app.schemas.booking_schema import CancelResponse

class BookingService:
    MAX_DAILY = 20

    @staticmethod
    async def book_seats(user_id: int, trip_id: int, seat_numbers: List[int], pay_with_wallet: bool = True):
        pool = await get_pool()

        async with pool.acquire() as conn:
            tr = conn.transaction()
            await tr.start()
            try:

                daily_count = await BookingRepo.get_user_daily_bookings_count(conn, user_id)
                if daily_count + len(seat_numbers) > BookingService.MAX_DAILY:
                    raise HTTPException(status_code=429, detail=f"Daily booking limit {BookingService.MAX_DAILY} exceeded")


                trip_row = await conn.fetchrow(
                    "SELECT price FROM trips WHERE id=$1 FOR UPDATE",
                    trip_id
                )
                if not trip_row:
                    raise HTTPException(status_code=404, detail="Trip not found")
                trip_price = trip_row["price"]
                total_amount = trip_price * len(seat_numbers)

                wallet_row = None
                if pay_with_wallet:
                    wallet_row = await BookingRepo.get_wallet_for_update(conn, user_id)
                    if not wallet_row:
                        raise HTTPException(status_code=400, detail="Wallet not found")
                    if wallet_row["balance"] < total_amount:
                        raise HTTPException(status_code=402, detail="Insufficient wallet balance")


                seat_numbers.sort()
                booking_ids = []

                for seat_no in seat_numbers:
                    seat_row = await BookingRepo.select_seat_for_update(conn, trip_id, seat_no)
                    if not seat_row:
                        raise HTTPException(status_code=404, detail=f"Seat {seat_no} not found")
                    if seat_row["status"] != "available":
                        raise HTTPException(status_code=409, detail=f"Seat {seat_no} already reserved")

                    booking_row = await BookingRepo.insert_booking(
                        conn, user_id, trip_id, seat_row["id"],
                        status="confirmed",
                        payment_status="paid" if pay_with_wallet else "pending"
                    )
                    booking_ids.append(booking_row["id"])

                    await BookingRepo.update_seat_booking(conn, seat_row["id"], "reserved")


                if pay_with_wallet:
                    new_balance = wallet_row["balance"] - total_amount
                    await BookingRepo.update_wallet_balance(conn, wallet_row["id"], new_balance)
                    await BookingRepo.insert_transaction(
                        conn,
                        user_id=user_id, wallet_id=wallet_row["id"],
                        related_booking_id=booking_ids[0], amount=total_amount,
                        ttype="debit", method="wallet", status="completed",
                        balance_after=new_balance
                    )
                else:
                    await BookingRepo.insert_transaction(
                        conn,
                        user_id=user_id, wallet_id=None,
                        related_booking_id=booking_ids[0], amount=total_amount,
                        ttype="debit", method="card", status="pending",
                        balance_after=(wallet_row["balance"] if wallet_row else 0)
                    )

                await tr.commit()
                return booking_ids

            except HTTPException:
                await tr.rollback()
                raise
            except Exception as e:
                await tr.rollback()
                raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def cancel_bookings(user_id: int, booking_ids: List[int]) -> CancelResponse:
        pool = await get_pool()
        async with pool.acquire() as conn:
            tr = conn.transaction()
            await tr.start()
            try:
                bookings = await BookingRepo.get_bookings_for_update(conn, booking_ids, user_id)
                if not bookings:
                    raise HTTPException(status_code=404, detail="No bookings found")

                wallet = await BookingRepo.get_wallet_for_update(conn, user_id)
                if not wallet:
                    raise HTTPException(status_code=400, detail="Wallet not found")

                new_balance = wallet["balance"]
                cancelled_ids = []
                now = datetime.datetime.utcnow()

                for b in bookings:
                    if b["status"] == "cancelled":
                        continue

                    if b["departure_time"] <= now.replace(tzinfo=b["departure_time"].tzinfo):
                        raise HTTPException(status_code=400, detail=f"Cannot cancel booking {b['id']} after departure")

                    await BookingRepo.update_booking_status(conn, b["id"], "cancelled", "refunded")
                    await BookingRepo.free_seat(conn, b["seat_id"])

                    new_balance += b["price"]
                    await BookingRepo.update_wallet_balance(conn, wallet["id"], new_balance)

                    await BookingRepo.insert_transaction(
                        conn, user_id, wallet["id"], b["id"], b["price"], "credit",
                        "wallet", "completed", new_balance
                    )

                    cancelled_ids.append(b["id"])

                await tr.commit()

                return CancelResponse(
                    status="cancelled",
                    wallet_balance=new_balance,
                    cancelled_bookings=cancelled_ids
                )

            except HTTPException:
                await tr.rollback()
                raise
            except Exception as e:
                await tr.rollback()
                raise HTTPException(status_code=500, detail=str(e))
