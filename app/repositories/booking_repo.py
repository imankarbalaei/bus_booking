from typing import List

class BookingRepo:
    @staticmethod
    async def get_user_daily_bookings_count(conn, user_id: int):
        row = await conn.fetchrow(
            "SELECT COUNT(*)::int AS cnt FROM bookings "
            "WHERE user_id=$1 AND created_at::date = CURRENT_DATE AND deleted_at IS NULL",
            user_id
        )
        return row["cnt"]

    @staticmethod
    async def select_seat_for_update(conn, trip_id: int, seat_number: int):
        return await conn.fetchrow(
            "SELECT id, status FROM seats WHERE trip_id=$1 AND seat_number=$2 FOR UPDATE",
            trip_id, seat_number
        )

    @staticmethod
    async def insert_booking(conn, user_id:int, trip_id:int, seat_id:int,
                             status:str, payment_status:str):
        return await conn.fetchrow(
            "INSERT INTO bookings(user_id, trip_id, seat_id, status, payment_status) "
            "VALUES($1,$2,$3,$4,$5) RETURNING id",
            user_id, trip_id, seat_id, status, payment_status
        )

    @staticmethod
    async def update_seat_booking(conn, seat_id:int, new_status:str='reserved'):
        await conn.execute(
            "UPDATE seats SET status=$1 WHERE id=$2",
            new_status, seat_id
        )

    @staticmethod
    async def get_wallet_for_update(conn, user_id:int):
        return await conn.fetchrow(
            "SELECT id, balance FROM wallets WHERE user_id=$1 FOR UPDATE",
            user_id
        )

    @staticmethod
    async def update_wallet_balance(conn, wallet_id:int, new_balance:int):
        await conn.execute(
            "UPDATE wallets SET balance=$1 WHERE id=$2",
            new_balance, wallet_id
        )

    @staticmethod
    async def insert_transaction(conn, user_id:int, wallet_id:int | None,
                                 related_booking_id:int | None, amount:int, ttype:str,
                                 method:str, status:str, balance_after:int):
        await conn.execute(
            "INSERT INTO transactions(user_id, wallet_id, related_booking_id, amount, type, method, status, wallet_balance_after) "
            "VALUES($1,$2,$3,$4,$5,$6,$7,$8)",
            user_id, wallet_id, related_booking_id, amount, ttype, method, status, balance_after
        )

    @staticmethod
    async def get_bookings_for_update(conn, booking_ids: List[int], user_id: int):
        return await conn.fetch(
            """
            SELECT b.id, b.user_id, b.trip_id, b.seat_id, b.status, b.payment_status, t.price, t.departure_time
            FROM bookings b
            JOIN trips t ON b.trip_id = t.id
            WHERE b.id = ANY($1::int[]) AND b.user_id = $2
            FOR UPDATE
            """,
            booking_ids, user_id
        )

    @staticmethod
    async def update_booking_status(conn, booking_id: int, status: str, payment_status: str):
        await conn.execute(
            "UPDATE bookings SET status=$1, payment_status=$2 WHERE id=$3",
            status, payment_status, booking_id
        )

    @staticmethod
    async def free_seat(conn, seat_id: int):
        await conn.execute(
            "UPDATE seats SET status='available' WHERE id=$1",
            seat_id
        )


