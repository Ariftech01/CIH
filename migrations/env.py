import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add parent directory to path so backend module can be loaded
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.config.settings import settings
from backend.database.base import Base
import backend.models  # Ensures all models are registered in Base metadata

config = getattr(context, "config", None)

if config and config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_db_url() -> str:
    url = (settings.DATABASE_URL or "").strip()
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


def run_migrations_offline() -> None:
    url = get_db_url()
    if not url:
        raise ValueError("DATABASE_URL environment variable is not configured for migrations.")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = get_db_url()
    if not url:
        raise ValueError("DATABASE_URL environment variable is not configured for migrations.")

    configuration = (config.get_section(config.config_ini_section) if config else {}) or {}
    configuration["sqlalchemy.url"] = url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if config is not None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()

