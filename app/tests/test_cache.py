import pytest
from fastapi import status
from app.core.cache import cache
from app.core.constants import CACHE_KEYS


def test_cache_set_get(client, test_user):
    """Test setting and getting from cache."""
    # Set cache
    cache.set(f"{CACHE_KEYS['USERS']}:{test_user.id}", test_user.__dict__)
    
    # Get from cache
    cached_user = cache.get(f"{CACHE_KEYS['USERS']}:{test_user.id}")
    assert cached_user is not None
    assert cached_user["id"] == test_user.id
    assert cached_user["nome"] == test_user.nome
    assert cached_user["email"] == test_user.email


def test_cache_delete(client, test_user):
    """Test deleting from cache."""
    # Set cache
    cache.set(f"{CACHE_KEYS['USERS']}:{test_user.id}", test_user.__dict__)
    
    # Delete from cache
    cache.delete(f"{CACHE_KEYS['USERS']}:{test_user.id}")
    
    # Try to get from cache
    cached_user = cache.get(f"{CACHE_KEYS['USERS']}:{test_user.id}")
    assert cached_user is None


def test_cache_clear(client, test_user, test_book):
    """Test clearing cache."""
    # Set multiple cache entries
    cache.set(f"{CACHE_KEYS['USERS']}:{test_user.id}", test_user.__dict__)
    cache.set(f"{CACHE_KEYS['BOOKS']}:{test_book.id}", test_book.__dict__)
    
    # Clear cache
    cache.clear()
    
    # Try to get from cache
    cached_user = cache.get(f"{CACHE_KEYS['USERS']}:{test_user.id}")
    cached_book = cache.get(f"{CACHE_KEYS['BOOKS']}:{test_book.id}")
    assert cached_user is None
    assert cached_book is None


def test_cache_expiration(client, test_user):
    """Test cache expiration."""
    # Set cache with short expiration
    cache.set(
        f"{CACHE_KEYS['USERS']}:{test_user.id}",
        test_user.__dict__,
        expire=1  # 1 second
    )
    
    # Wait for expiration
    import time
    time.sleep(2)
    
    # Try to get from cache
    cached_user = cache.get(f"{CACHE_KEYS['USERS']}:{test_user.id}")
    assert cached_user is None


def test_cache_connection_error():
    """Test cache connection error handling."""
    # Temporarily disable Redis connection
    original_redis = cache.redis
    cache.redis = None
    
    # Try to set cache
    result = cache.set("test_key", "test_value")
    assert result is False
    
    # Try to get from cache
    value = cache.get("test_key")
    assert value is None
    
    # Restore Redis connection
    cache.redis = original_redis 