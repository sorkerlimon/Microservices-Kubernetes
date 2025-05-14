"""
Redis cache utilities.
"""

import os
import json
import logging
import redis
import time

logger = logging.getLogger(__name__)

# Redis connection
REDIS_HOST = os.getenv("REDIS_HOST", "kub-cache")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# Set a global redis_client variable
redis_client = None

# Try to connect to Redis with retry logic
max_retries = 5
retry_interval = 2  # seconds

for retry in range(max_retries):
    try:
        # Create Redis client with socket timeout
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True,  # Automatically decode responses to Python strings
            socket_timeout=5,  # Add timeout for socket operations
            socket_connect_timeout=5,  # Add timeout for connection
            retry_on_timeout=True  # Retry on timeout
        )
        
        # Test Redis connection
        redis_ping = redis_client.ping()
        logger.info(f"Redis connection successful: {redis_ping}")
        break  # Connection successful, exit retry loop
    except Exception as e:
        logger.warning(f"Redis connection attempt {retry+1}/{max_retries} failed: {e}")
        if retry < max_retries - 1:
            logger.info(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
        else:
            logger.error(f"Failed to connect to Redis after {max_retries} attempts: {e}")
            # Initialize a dummy client that logs operations but doesn't fail
            class DummyRedis:
                def __getattr__(self, name):
                    def dummy_method(*args, **kwargs):
                        logger.debug(f"Redis operation '{name}' called, but Redis is unavailable")
                        return None
                    return dummy_method
            
            redis_client = DummyRedis()

# Cache helper functions
def cache_get(key):
    """Get data from cache."""
    try:
        data = redis_client.get(key)
        if data:
            logger.info(f"Cache hit for key: {key}")
            return json.loads(data)
        logger.info(f"Cache miss for key: {key}")
        return None
    except Exception as e:
        logger.error(f"Cache error getting {key}: {str(e)}")
        return None

def cache_set(key, value, expiry=3600):
    """Set data in cache with expiry in seconds."""
    try:
        redis_client.setex(key, expiry, json.dumps(value))
        logger.info(f"Set cache for key: {key} with expiry: {expiry}s")
        return True
    except Exception as e:
        logger.error(f"Cache error setting {key}: {str(e)}")
        return False

def cache_delete(key):
    """Delete data from cache."""
    try:
        redis_client.delete(key)
        logger.info(f"Deleted cache for key: {key}")
        return True
    except Exception as e:
        logger.error(f"Cache error deleting {key}: {str(e)}")
        return False

def cache_invalidate_pattern(pattern):
    """Invalidate all keys matching a pattern."""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            logger.info(f"Invalidated {len(keys)} keys matching pattern: {pattern}")
        return True
    except Exception as e:
        logger.error(f"Cache error invalidating pattern {pattern}: {str(e)}")
        return False 