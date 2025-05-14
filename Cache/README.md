# Redis Cache Server

This directory contains configuration for a Redis cache server using Docker.

## Build and Run

### Build the Docker image

```bash
cd Cache
docker build -t kub-redis .
```

### Run the Redis container

```bash
docker run -d --name kub-cache -p 6379:6379 kub-redis
```

## Accessing Redis

### Using Redis CLI from the container

```bash
docker exec -it kub-cache redis-cli
```

### Using Redis CLI from your host (if you have redis-cli installed)

```bash
redis-cli -h localhost -p 6379
```

## Basic Redis Commands

Once you're in the Redis CLI, you can use these commands:

### Set a key-value pair

```
SET key value
```

Example:
```
SET user:1:name "Limon"
```

### Get a value by key

```
GET key
```

Example:
```
GET user:1:name
```

### Delete a key

```
DEL key
```

### Check if a key exists

```
EXISTS key
```

### Set an expiring key (TTL in seconds)

```
SETEX key seconds value
```

Example:
```
SETEX session:123 3600 "user_session_data"
```

### List all keys matching a pattern

```
KEYS pattern
```

Example:
```
KEYS user:*
```

### Increment a counter

```
INCR counter_key
```

## Using Redis with your Backend

In your backend code, you'll need to use a Redis client library. For Python with FastAPI, use:

```python
import redis

# Connect to Redis
redis_client = redis.Redis(host='cache', port=6379, db=0)

# Example cache function
def get_cached_data(key):
    cached_data = redis_client.get(key)
    if cached_data:
        return cached_data
    # Get data from database if not in cache
    data = get_data_from_db()
    # Cache the data (expire in 1 hour)
    redis_client.setex(key, 3600, data)
    return data
```

## Docker Compose Integration

Update your docker-compose.yml to include Redis:

```yaml
services:
  cache:
    build: ./Cache
    ports:
      - "6379:6379"
```

Connect to Redis from other containers using the service name 'cache' as the hostname. 