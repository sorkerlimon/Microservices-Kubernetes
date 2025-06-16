# Dockerfile for Django Backend
# Uses slim Python image for smaller footprint

FROM python:3.12-slim

# Avoid Python buffering & .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps (gcc & mysql client libs for mysql-connector)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies separately for better caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project code
COPY . .

# Collect static files (no input to avoid prompt) – ignore if none
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run migrations & start gunicorn via entrypoint
CMD ["/bin/sh", "-c", "python manage.py migrate && gunicorn backfontend.wsgi:application --bind 0.0.0.0:8000"]
