from fastapi import HTTPException
from typing import List
from app.repositories.booking_repo import BookingRepo
from app.db.database import get_pool,pool
from app.db.database import fetch,fetchrow,execute

class BookingService:
    MAX_DAILY = 20

    @staticmethod
    async def book_seats(user_id: int, trip_id: int, seat_numbers: List[int], pay_with_wallet: bool = True):

        pool = await get_pool()
        async with pool.acquire() as conn:
            tr = conn.transaction()
            await tr.start()

            try:

                daily_count = await BookingRepo.get_user_daily_bookings_count(user_id)
                if daily_count + len(seat_numbers) > BookingService.MAX_DAILY:
                    raise HTTPException(status_code=429, detail=f"Daily booking limit {BookingService.MAX_DAILY} exceeded")


                trip_row = await fetchrow(
                    "SELECT price FROM trips WHERE id=$1 FOR UPDATE",
                    trip_id
                )
                if not trip_row:
                    raise HTTPException(status_code=404, detail="Trip not found")
                trip_price = trip_row["price"]
                total_amount = trip_price * len(seat_numbers)


                wallet_row = None
                if pay_with_wallet:
                    wallet_row = await BookingRepo.get_wallet_for_update(user_id)
                    if not wallet_row:
                        raise HTTPException(status_code=400, detail="Wallet not found")
                    if wallet_row["balance"] < total_amount:
                        raise HTTPException(status_code=402, detail="Insufficient wallet balance")

                booking_ids = []


                for seat_no in seat_numbers:
                    seat_row = await BookingRepo.select_seat_for_update(trip_id, seat_no)
                    if not seat_row:
                        await tr.rollback()
                        raise HTTPException(status_code=404, detail=f"Seat {seat_no} not found")
                    if seat_row["status"] != "available":
                        await tr.rollback()
                        raise HTTPException(status_code=409, detail=f"Seat {seat_no} already reserved")

                    # insert booking
                    booking_row = await BookingRepo.insert_booking(
                        conn, user_id, trip_id, seat_row["id"],
                        status="confirmed",
                        payment_status="paid" if pay_with_wallet else "pending"
                    )
                    booking_ids.append(booking_row["id"])


                    await BookingRepo.update_seat_booking(seat_row["id"], new_status="reserved")


                if pay_with_wallet:
                    new_balance = wallet_row["balance"] - total_amount
                    await BookingRepo.update_wallet_balance(wallet_row["id"], new_balance)
                    await BookingRepo.insert_transaction(
                        user_id=user_id, wallet_id=wallet_row["id"],
                        related_booking_id=booking_ids[0], amount=total_amount,
                        ttype="debit", method="wallet", status="completed",
                        balance_after=new_balance
                    )
                else:
                    await BookingRepo.insert_transaction(
                        user_id=user_id, wallet_id=None,
                        related_booking_id=booking_ids[0], amount=total_amount,
                        ttype="debit", method="card", status="pending",
                        balance_after=(wallet_row["balance"] if wallet_row else 0)
                    )

                await tr.commit()

                return booking_ids

            except HTTPException:
                raise
            except Exception as e:
                await tr.rollback()
                raise HTTPException(status_code=500, detail=str(e))



    @staticmethod
    async def cancel_booking(user_id: int, booking_id: int):
        pool = await get_pool()
        async with pool.acquire() as conn:
            tr = conn.transaction()
            await tr.start()
            try:
                # 1) fetch booking (with trip info)
                booking = await fetchrow(
                    "SELECT b.id, b.user_id, b.trip_id, b.seat_id, b.status, t.departure_time, t.price FROM bookings b JOIN trips t ON b.trip_id=t.id WHERE b.id=$1 FOR UPDATE",
                    booking_id
                )
                if not booking:
                    raise HTTPException(status_code=404, detail="Booking not found")
                if booking["user_id"] != user_id:
                    raise HTTPException(status_code=403, detail="Not owner of booking")
                # cannot cancel after departure
                import datetime
                if booking["departure_time"] <= datetime.datetime.utcnow().astimezone(
                        booking["departure_time"].tzinfo):
                    raise HTTPException(status_code=400, detail="Cannot cancel after departure")

                # update booking status and payment_status
                await execute("UPDATE bookings SET status=$1, payment_status=$2 WHERE id=$3",
                                   'cancelled', 'refunded', booking_id)
                # free seat
                await execute("UPDATE seats SET booking_id=NULL, status=$1 WHERE id=$2", 'available',
                                   booking["seat_id"])

                # refund wallet (simplified: find wallet and update)
                wallet_row = await fetchrow("SELECT id, balance FROM wallets WHERE user_id=$1 FOR UPDATE",
                                                 user_id)
                if wallet_row:
                    new_balance = wallet_row["balance"] + booking["price"]
                    await execute("UPDATE wallets SET balance=$1 WHERE id=$2", new_balance,
                                       wallet_row["id"])
                    await execute(
                        "INSERT INTO transactions(user_id, wallet_id, related_booking_id, amount, type, method, status, wallet_balance_after) "
                        "VALUES($1,$2,$3,$4,$5,$6,$7,$8)",
                        user_id, wallet_row["id"], booking_id, booking["price"], 'credit', 'wallet',
                        'completed', new_balance
                    )
                await tr.commit()
            except HTTPException:
                raise
            except Exception as e:
                await tr.rollback()
                raise HTTPException(status_code=500, detail=str(e))

