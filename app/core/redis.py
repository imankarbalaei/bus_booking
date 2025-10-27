# from redis.asyncio import Redis
# from app.core.config import settings
#
# class RedisClient:
#     def __init__(self):
#         self.redis: Redis | None = None
#
#     async def connect(self):
#         self.redis = Redis.from_url(
#             settings.REDIS_URL,
#             decode_responses=True
#         )
#
#         try:
#             await self.redis.ping()
#             print("Redis connected!")
#         except Exception as e:
#             print("Redis connection failed:", e)
#             raise e
#
#     async def disconnect(self):
#         if self.redis:
#             await self.redis.close()
#             print("Redis disconnected!")
#
#
# redis_client = RedisClient()
