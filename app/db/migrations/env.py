import sys
import os
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import create_engine

from alembic import context


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


from app.core.config import settings
from app.db.database import Base
from app.models import (
    user_model,
    operator_model,
    bus_model,
    trip_model,
    booking_model,
    wallet_model,
    transaction_model,
    route_model,
    city_model,
)

target_metadata = Base.metadata


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode for async SQLAlchemy."""
    connectable = AsyncEngine(
        create_engine(settings.DATABASE_URL, poolclass=pool.NullPool, future=True)
    )

    asyncio.run(do_run_migrations(connectable))


async def do_run_migrations(connectable: AsyncEngine) -> None:
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations_sync)


def do_run_migrations_sync(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
