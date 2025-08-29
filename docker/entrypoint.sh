#!/usr/bin/env bash
set -euo pipefail

# Ensure runtime dirs exist (idempotent)
mkdir -p storage/framework/cache storage/framework/sessions storage/framework/views bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache || true
chmod -R ug+rwX storage bootstrap/cache || true

# Only run migrations on boot when explicitly enabled
if [[ "${RUN_MIGRATIONS_ON_BOOT:-false}" == "false" ]]; then
  echo "[entrypoint] Running database migrations..."
  php artisan migrate --force --no-interaction || true
fi

# Cache configs/routes/views for performance (ignore failures if not writable)
php artisan config:cache || true
php artisan route:cache || true
php artisan view:cache || true

# Set proper permissions
echo "Setting proper permissions..."
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html
chmod -R 775 storage bootstrap/cache

echo "Laravel application is ready!"
# Start Apache in foreground
exec apache2-foreground
