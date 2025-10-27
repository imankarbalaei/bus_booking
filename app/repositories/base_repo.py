#
# class BaseRepository:
#     def __init__(self, pool):
#         self.pool = pool
#
#     async def fetchrow(self, query, *args):
#         async with self.pool.acquire() as conn:
#             return await conn.fetchrow(query, *args)
#
#     async def fetch(self, query, *args):
#         async with self.pool.acquire() as conn:
#             return await conn.fetch(query, *args)
#
#     async def execute(self, query, *args):
#         async with self.pool.acquire() as conn:
#             return await conn.execute(query, *args)
#
#     async def transaction(self):
#         return self.pool.acquire()
