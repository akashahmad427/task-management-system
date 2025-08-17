#!/bin/bash

# Railway startup script for Django
echo "Starting Django application..."

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting Gunicorn..."
gunicorn task_management_system.wsgi:application 