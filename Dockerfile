# Use Python 3.12 base image
FROM python:3.12-slim AS base

# Install system dependencies (only necessary ones)
RUN apt-get update && apt-get install -y \
    libgtk-3-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port Django runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
