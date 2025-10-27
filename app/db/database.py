import asyncpg
from app.core.config import settings

from sqlalchemy.orm import declarative_base

Base = declarative_base()

pool: asyncpg.Pool | None = None

async def get_pool() -> asyncpg.Pool:
    global pool
    if pool is None:
        await connect_db()
    return pool


async def connect_db():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL, min_size=2, max_size=20)
    return pool

async def disconnect_db():
    global pool
    if pool:
        await pool.close()
        pool = None

async def fetch(query: str, *args):
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)

async def fetchrow(query: str, *args):
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *args)

async def execute(query: str, *args):
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)