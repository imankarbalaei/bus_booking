from typing import List
import asyncpg
from app.db.database import fetch,fetchrow,execute

class BookingRepo:
    @staticmethod
    async def get_user_daily_bookings_count(user_id: int):
        row = await fetchrow(
            "SELECT COUNT(*)::int AS cnt FROM bookings "
            "WHERE user_id=$1 AND created_at::date = CURRENT_DATE AND deleted_at IS NULL",
            user_id
        )
        return row["cnt"]

    @staticmethod
    async def select_seat_for_update(trip_id: int, seat_number: int):
        # lock the seat row
        return await fetchrow(
            "SELECT id, status FROM seats WHERE trip_id=$1 AND seat_number=$2 FOR UPDATE",
            trip_id, seat_number
        )

    @staticmethod
    async def insert_booking(user_id:int, trip_id:int, seat_id:int,
                             status:str='confirmed', payment_status:str='paid'):
        return await fetchrow(
            "INSERT INTO bookings(user_id, trip_id, seat_id, status, payment_status) "
            "VALUES($1,$2,$3,$4,$5) RETURNING id",
            user_id, trip_id, seat_id, status, payment_status
        )

    @staticmethod
    async def update_seat_booking(seat_id:int, new_status:str='reserved'):
        await execute(
            "UPDATE seats SET status=$1 WHERE id=$2",
            new_status, seat_id
        )

    @staticmethod
    async def get_wallet_for_update(user_id:int):
        # lock wallet row
        return await fetchrow(
            "SELECT id, balance FROM wallets WHERE user_id=$1 FOR UPDATE",
            user_id
        )

    @staticmethod
    async def update_wallet_balance(wallet_id:int, new_balance:int):
        await execute(
            "UPDATE wallets SET balance=$1 WHERE id=$2",
            new_balance, wallet_id
        )

    @staticmethod
    async def insert_transaction(user_id:int, wallet_id:int | None,
                                 related_booking_id:int | None, amount:int, ttype:str,
                                 method:str, status:str, balance_after:int):
        await execute(
            "INSERT INTO transactions(user_id, wallet_id, related_booking_id, amount, type, method, status, wallet_balance_after) "
            "VALUES($1,$2,$3,$4,$5,$6,$7,$8)",
            user_id, wallet_id, related_booking_id, amount, ttype, method, status, balance_after
        )
