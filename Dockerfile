# syntax=docker/dockerfile:1

FROM php:8.2-apache

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git unzip libzip-dev libpng-dev libicu-dev \
  && rm -rf /var/lib/apt/lists/*

# PHP extensions commonly used by Laravel
RUN docker-php-ext-install -j"$(nproc)" \
    pdo_mysql \
    bcmath \
    exif \
    intl \
    zip \
    opcache

# Apache: set DocumentRoot to /public and enable rewrite
ENV APACHE_DOCUMENT_ROOT=/var/www/html/public
RUN sed -ri -e 's!/var/www/html!/var/www/html/public!g' \
      /etc/apache2/sites-available/000-default.conf /etc/apache2/apache2.conf \
  && a2enmod rewrite

WORKDIR /var/www/html

# Install Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Install PHP dependencies (use build cache). Do not run scripts yet because app files aren't copied.
COPY composer.json composer.lock ./
RUN composer install --no-dev --prefer-dist --no-progress --no-interaction --no-scripts

# Copy the rest of the application
COPY . .

# Now that the full app (including artisan) exists, run post-install scripts and optimize
RUN composer dump-autoload --optimize && \
    composer run-script post-autoload-dump || true

# Copy entrypoint and make it executable
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Ensure runtime directories exist and set permissions for Laravel
RUN set -eux; \
    mkdir -p storage/framework/cache storage/framework/sessions storage/framework/views bootstrap/cache; \
    chown -R www-data:www-data storage bootstrap/cache

# Production defaults (override via env at runtime)
ENV APP_ENV=production \
    APP_DEBUG=0 \
    LOG_CHANNEL=stderr

EXPOSE 80
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]


