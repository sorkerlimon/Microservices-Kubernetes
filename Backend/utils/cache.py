"""
Redis cache utilities.
"""

import os
import json
import logging
import redis

logger = logging.getLogger(__name__)

# Redis connection
REDIS_HOST = os.getenv("REDIS_HOST", "kub-cache")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

try:
    # Create Redis client
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True  # Automatically decode responses to Python strings
    )
    
    # Test Redis connection
    redis_ping = redis_client.ping()
    logger.info(f"Redis connection successful: {redis_ping}")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    # Continue without Redis if it fails

# Cache helper functions
def cache_get(key):
    """Get data from cache."""
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.error(f"Cache error: {str(e)}")
        return None

def cache_set(key, value, expiry=3600):
    """Set data in cache with expiry in seconds."""
    try:
        redis_client.setex(key, expiry, json.dumps(value))
        return True
    except Exception as e:
        logger.error(f"Cache error: {str(e)}")
        return False

def cache_delete(key):
    """Delete data from cache."""
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Cache error: {str(e)}")
        return False

def cache_invalidate_pattern(pattern):
    """Invalidate all keys matching a pattern."""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
        return True
    except Exception as e:
        logger.error(f"Cache error: {str(e)}")
        return False 