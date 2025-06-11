import json
import logging
from typing import Any, Optional
import redis

from app.core.config import settings


class Cache:
    """Redis cache implementation."""
    
    def __init__(self) -> None:
        """Initialize cache connection."""
        try:
            self.redis = redis.from_url(settings.REDIS_URL)
            self.logger = logging.getLogger("library_api")
        except redis.ConnectionError as e:
            self.logger.error(f"Failed to connect to Redis: {str(e)}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key (str): Cache key.
            
        Returns:
            Optional[Any]: Cached value or None if not found.
        """
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode cached value: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Cache get error: {str(e)}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """Set value in cache.
        
        Args:
            key (str): Cache key.
            value (Any): Value to cache.
            expire (Optional[int]): Expiration time in seconds.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            serialized = json.dumps(value)
            if expire:
                return bool(self.redis.setex(key, expire, serialized))
            return bool(self.redis.set(key, serialized))
        except Exception as e:
            self.logger.error(f"Cache set error: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache.
        
        Args:
            key (str): Cache key.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            self.logger.error(f"Cache delete error: {str(e)}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache entries.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            return bool(self.redis.flushdb())
        except Exception as e:
            self.logger.error(f"Cache clear error: {str(e)}")
            return False


# Create cache instance
cache = Cache() 