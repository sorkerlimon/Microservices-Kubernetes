# Use the official Redis image
FROM redis:8.0-alpine3.21

# Set a custom configuration (optional)
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose Redis port
EXPOSE 6379

# Run Redis with the custom config
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
