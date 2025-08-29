# syntax=docker/dockerfile:1

FROM php:8.0-apache

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git unzip \
    libzip-dev libpng-dev libjpeg-dev libfreetype6-dev \
    libicu-dev libxml2-dev libxslt1-dev \
    libcurl4-openssl-dev libonig-dev libssl-dev \
    libsqlite3-dev libbz2-dev libgettextpo-dev \
  && rm -rf /var/lib/apt/lists/*

# PHP extensions commonly used by Laravel/Lumen and requested list
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
  && docker-php-ext-install -j"$(nproc)" \
    bcmath \
    bz2 \
    calendar \
    curl \
    exif \
    ftp \
    gd \
    gettext \
    intl \
    mbstring \
    mysqli \
    opcache \
    pdo_mysql \
    shmop \
    soap \
    sockets \
    sysvmsg \
    sysvsem \
    sysvshm \
    xsl \
    zip

# Apache: set DocumentRoot to /public and enable rewrite
ENV APACHE_DOCUMENT_ROOT=/var/www/html/public
RUN sed -ri -e 's!/var/www/html!/var/www/html/public!g' \
      /etc/apache2/sites-available/000-default.conf /etc/apache2/apache2.conf \
  && a2enmod rewrite

WORKDIR /var/www/html

# Install Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Copy the rest of the application
COPY . .

# If a Composer project is present, install dependencies without running scripts yet
RUN if [ -f composer.json ]; then \
        composer install --no-dev --prefer-dist --no-progress --no-interaction --no-scripts; \
    fi

# Now that the full app exists, run post-install scripts and optimize (only if composer.json exists)
RUN if [ -f composer.json ]; then \
        composer dump-autoload --optimize; \
        composer run-script post-autoload-dump || true; \
    fi

# Copy entrypoint and make it executable
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Ensure runtime directories exist and set permissions for Laravel
RUN set -eux; \
    mkdir -p storage/framework/cache storage/framework/sessions storage/framework/views storage/logs bootstrap/cache; \
    chown -R www-data:www-data storage bootstrap/cache; \
    chmod -R ug+rwX storage bootstrap/cache

# Production defaults (override via env at runtime)
ENV APP_ENV=production \
    APP_DEBUG=0 \
    LOG_CHANNEL=stderr

EXPOSE 80
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]


