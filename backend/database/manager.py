from typing import Dict, Any
from backend.database.engine import get_engine
from backend.database.session import SessionFactory, SessionLocal, ScopedSession, get_db_session
from backend.database.connection import check_connection, ping_database
from backend.app_logging.logger import db_logger
from backend.config.settings import settings


class DatabaseManager:
    """
    Centralized Singleton Database Connection & Lifecycle Manager for CIH Backend.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.session_factory = SessionFactory
            cls._instance.session_local = SessionLocal
            cls._instance.scoped_session = ScopedSession
        return cls._instance

    @property
    def engine(self):
        return get_engine()

    def create_all_tables(self):
        """
        Creates all PostgreSQL tables defined in Base metadata if missing.
        """
        from backend.database.base import Base
        import backend.models  # Ensures all SQLAlchemy models are registered in Base.metadata
        eng = self.engine
        if eng is None:
            db_logger.warning("Database engine is not initialized; skipping create_all_tables.")
            return
        try:
            Base.metadata.create_all(bind=eng)
            db_logger.info("Database tables initialized (for test/local isolated environments).")
        except Exception as e:
            db_logger.error(f"Failed to create database tables: {str(e)}")
            raise

    def drop_all_tables(self):
        """
        Drops all tables (use with caution in test/reset scenarios).
        """
        from backend.database.base import Base
        import backend.models  # Ensures all SQLAlchemy models are registered in Base.metadata
        eng = self.engine
        if eng is None:
            return
        try:
            Base.metadata.drop_all(bind=eng)
            db_logger.warning("All database tables dropped successfully.")
        except Exception as e:
            db_logger.error(f"Failed to drop database tables: {str(e)}")
            raise


    def is_healthy(self) -> bool:
        return check_connection()

    def check_health(self) -> Dict[str, Any]:
        """
        Returns full diagnostic health status of the database backend.
        """
        conn_ok = check_connection()
        return {
            "status": "Healthy" if conn_ok else "Critical",
            "database_connected": conn_ok,
            "environment": settings.APP_ENV,
            "database_url_configured": bool(settings.DATABASE_URL),
            "supabase_configured": bool(settings.SUPABASE_URL),
            "ssl_enabled": settings.SSL_MODE != "disable",
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW
        }

    def get_session_context(self):
        return get_db_session()

    def dispose(self):
        """
        Gracefully disposes engine connections.
        """
        eng = self.engine
        if eng is not None:
            eng.dispose()
            db_logger.info("Database engine connections disposed gracefully.")

db_manager = DatabaseManager()
