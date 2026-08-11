"""Database configuration properties for connection pooling and dialect options."""

from .settings import settings


def get_engine_options():
    """Return enterprise PostgreSQL engine configuration options for connection pooling."""
    return {
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "pool_recycle": settings.DB_POOL_RECYCLE,
        "pool_pre_ping": True,
        "echo": settings.DEBUG,
    }
