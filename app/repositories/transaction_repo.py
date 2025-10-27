# from .base_repo import BaseRepository
# from app.db.database import db
# from datetime import datetime
#
# class TransactionRepository(BaseRepository):
#     def __init__(self):
#         super().__init__(db.pool)
#
#     async def create(
#         self,
#         user_id: int,
#         amount: int,
#         type: str,
#         method: str,
#         status: str,
#         pool=None
#     ):
#         pool = pool or self.pool
#         query = """
#         INSERT INTO transactions(
#             user_id, amount, type, method, status, wallet_balance_after, created_at
#         )
#         VALUES($1, $2, $3, $4, $5,
#                (SELECT balance FROM wallets WHERE user_id=$1), NOW())
#         RETURNING id
#         """
#         async with pool.acquire() as conn:
#             return await conn.fetchrow(query, user_id, amount, type, method, status)
#
#     async def get_user_transactions(self, user_id: int, pool=None):
#         pool = pool or self.pool
#         query = """
#         SELECT * FROM transactions
#         WHERE user_id=$1 AND deleted_at IS NULL
#         ORDER BY created_at DESC
#         """
#         async with pool.acquire() as conn:
#             return await conn.fetch(query, user_id)
