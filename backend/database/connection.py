from sqlalchemy import text
from backend.database.engine import get_engine
from backend.app_logging.logger import db_logger
from backend.utils.exceptions import DatabaseConnectionError


def check_connection() -> bool:
    """Perform a lightweight ping query against the configured database engine."""
    engine = get_engine()
    if engine is None:
        return False

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        db_logger.error(f"Database health check failed: {str(e)}")
        return False

def ping_database():
    """
    Raises DatabaseConnectionError if the database is unreachable.
    """
    if not check_connection():
        raise DatabaseConnectionError("Database ping failed. Service is unavailable.")
    return True
