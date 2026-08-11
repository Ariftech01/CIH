from typing import Tuple, Dict, Any, Callable
import functools
from backend.app_logging.logger import logger
from backend.utils.exceptions import CIHBaseException

def handle_backend_errors(func: Callable) -> Callable:
    """
    Decorator for service & repository methods to catch exceptions, 
    log them cleanly, and return safe error responses.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CIHBaseException as e:
            logger.warning(f"Business Exception in {func.__name__}: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unhandled Exception in {func.__name__}: {str(e)}", exc_info=True)
            raise CIHBaseException(f"An internal error occurred in {func.__name__}") from e
    return wrapper
