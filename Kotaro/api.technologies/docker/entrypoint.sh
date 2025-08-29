#!/usr/bin/env bash
set -euo pipefail

# Ensure runtime dirs exist (idempotent)
mkdir -p storage/framework/cache storage/framework/sessions storage/framework/views storage/logs bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache || true
chmod -R ug+rwX storage bootstrap/cache || true
# Fallback for Windows bind mounts: make sure logs dir is world-writable
chmod -R 777 storage storage/logs bootstrap/cache 

# Only run migrations on boot when explicitly enabled
if [[ "${RUN_MIGRATIONS_ON_BOOT:-false}" == "false" ]]; then
  echo "[entrypoint] Running database migrations..."
  php artisan migrate --force --no-interaction || true
fi

# Cache configs/routes/views for performance (ignore failures if not writable)

php artisan config:cache || true
php artisan route:cache || true
php artisan view:cache || true

# Ensure today's log file exists and is writable by the web server
LOGFILE="storage/logs/lumen-$(date +%F).log"
touch "$LOGFILE" 2>/dev/null || true
chown -R www-data:www-data storage 2>/dev/null || true
chmod 666 "$LOGFILE" 2>/dev/null || true

# Start Apache in foreground
exec apache2-foreground