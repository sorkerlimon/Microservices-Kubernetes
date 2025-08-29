#!/bin/bash

# Exit on any error
set -e

echo "Starting Laravel 8 application setup..."

# Wait for database connection (if using MySQL/PostgreSQL)
echo "Waiting for database connection..."
until php artisan tinker --execute="DB::connection()->getPdo();" 2>/dev/null; do
    echo "Database not ready, waiting 2 seconds..."
    sleep 2
done

echo "Database connection established!"

# Generate application key if not exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

# Generate app key if not set
php artisan key:generate --no-interaction

# Clear all caches
echo "Clearing application caches..."
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear

# Cache configuration for better performance
echo "Caching configuration..."
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Create symbolic link for storage (if not exists)
if [ ! -L public/storage ]; then
    echo "Creating storage symbolic link..."
    php artisan storage:link
fi

# Set proper permissions
echo "Setting proper permissions..."
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html
chmod -R 775 storage bootstrap/cache

echo "Laravel application is ready!"

# Execute the main command
exec "$@"