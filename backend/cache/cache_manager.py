import time
from typing import Dict, Any, Optional

class CacheManager:
    """
    In-memory TTL & LRU cache manager with key-based invalidation.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
            cls._instance._cache: Dict[str, Dict[str, Any]] = {}
        return cls._instance

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry["expires_at"]:
                return entry["value"]
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl_seconds
        }

    def invalidate(self, key_prefix: str = None):
        if not key_prefix:
            self._cache.clear()
        else:
            keys_to_del = [k for k in self._cache if k.startswith(key_prefix)]
            for k in keys_to_del:
                del self._cache[k]

cache_manager = CacheManager()
