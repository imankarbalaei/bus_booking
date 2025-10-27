import sys
import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from alembic import context

# مسیر پروژه
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from app.core.config import settings
from app.db.database import Base
from app.models import (
    user_model,
    operator_model,
    bus_model,
    trip_model,
    seat_model,
    booking_model,
    wallet_model,
    transaction_model,
    route_model,
    city_model,

)

# metadata مدل‌ها
target_metadata = Base.metadata

# تنظیمات alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Offline migration"""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online migration with async engine"""
    # تبدیل postgresql:// -> postgresql+asyncpg://
    url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    connectable = create_async_engine(url, poolclass=pool.NullPool, future=True)

    asyncio.run(do_run_migrations(connectable))


async def do_run_migrations(connectable: AsyncEngine) -> None:
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations_sync)


def do_run_migrations_sync(connection: Connection) -> None:
    """Sync part Alembic"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # بررسی تغییرات type
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
