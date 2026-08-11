"""
Database Initialization Script for Construction Intelligence Hub (CIH).
Verifies database connection, registers models, and creates all tables.
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.database.manager import db_manager
from backend.database.connection import ping_database
from backend.app_logging.logger import logger

def init_db():
    logger.info("Initializing Construction Intelligence Hub (CIH) Database Foundation...")
    try:
        if ping_database():
            logger.info("Database ping successful.")
            db_manager.create_all_tables()
            logger.info("All database tables initialized successfully.")
            return True
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = init_db()
    if not success:
        sys.exit(1)
