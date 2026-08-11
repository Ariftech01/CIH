"""Performance profiler utility for CIH runtime diagnostics."""

import time
import functools
from typing import Callable, Any, Dict
from backend.app_logging.logger import logger

_PROFILER_RESULTS: Dict[str, float] = {}

def profile_func(name: str = None):
    """Decorator to profile execution time of functions."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            metric_name = name or f"{func.__module__}.{func.__qualname__}"
            t0 = time.perf_counter()
            try:
                res = func(*args, **kwargs)
                return res
            finally:
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                _PROFILER_RESULTS[metric_name] = round(elapsed_ms, 2)
                logger.debug(f"[PROFILER] {metric_name}: {elapsed_ms:.2f} ms")
        return wrapper
    return decorator

def get_profile_results() -> Dict[str, float]:
    """Return dictionary of recorded profile metrics."""
    return dict(_PROFILER_RESULTS)
