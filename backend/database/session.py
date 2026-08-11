from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from backend.database.engine import engine
from backend.app_logging.logger import db_logger
from backend.utils.exceptions import DatabaseConnectionError

# Central Session Factory
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

# Reusable SessionLocal Factory alias
SessionLocal = SessionFactory

# Thread-safe Scoped Session
ScopedSession = scoped_session(SessionFactory)

@contextmanager
def get_db_session():
    """
    Context manager for safe transactional database sessions per request/workflow.
    Automatically handles commit on success, rollback on error, and cleanup.
    """
    session: Session = ScopedSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        db_logger.error(f"Database session transaction failed, rolled back: {str(e)}")
        raise
    finally:
        session.close()
        ScopedSession.remove()

def get_session() -> Session:
    """
    Returns a new session instance from SessionLocal (caller is responsible for closing or committing).
    """
    return SessionLocal()
