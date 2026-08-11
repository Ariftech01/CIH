from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from backend.config.settings import settings
from backend.config.database import get_engine_options
from backend.app_logging.logger import db_logger
from backend.utils.exceptions import DatabaseConnectionError


engine: Optional[Engine] = None


def create_db_engine():
    """Create the centralized SQLAlchemy engine connecting to Neon PostgreSQL."""
    global engine

    try:
        database_url = (settings.DATABASE_URL or "").strip()
        if not database_url:
            engine = None
            db_logger.warning("DATABASE_URL is not configured; database engine initialization deferred")
            return engine

        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        options = get_engine_options()
        engine = create_engine(database_url, **options)
        target = database_url.split("@")[-1] if "@" in database_url else database_url
        db_logger.info(f"Initialized SQLAlchemy Engine for PostgreSQL database target: {target}")
        return engine
    except Exception as e:
        db_logger.error(f"Failed to create SQLAlchemy PostgreSQL engine: {str(e)}")
        if "psycopg2" in str(e) or "driver" in str(e).lower() or "dialect" in str(e).lower():
            db_logger.warning("SQLAlchemy PostgreSQL driver is unavailable; runtime remains configurable")
            return None
        raise DatabaseConnectionError(f"Could not connect to database engine: {str(e)}")


def get_engine() -> Optional[Engine]:
    """Return the cached engine, creating it on demand when a database URL is configured."""
    global engine
    if engine is None:
        return create_db_engine()
    return engine


engine = create_db_engine()
