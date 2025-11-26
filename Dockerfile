# Use official Python slim image
FROM python:3.10-slim-bookworm

# Set working directory
WORKDIR /app

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y \
        build-essential \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
        libssl-dev \
        ansible \
        netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose Django port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
    CMD nc -z localhost 8000 || exit 1

# Run migrations & start Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

