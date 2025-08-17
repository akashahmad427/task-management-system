#!/bin/bash

# Railway startup script for Django
echo "Starting Django application..."

# Wait for database to be ready
echo "Waiting for database connection..."
echo "Checking database configuration..."

# Debug environment variables
echo "Environment variables:"
echo "DATABASE_URL: $DATABASE_URL"
echo "RAILWAY_ENVIRONMENT: $RAILWAY_ENVIRONMENT"
echo "All environment variables:"
env | sort

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set!"
    echo "Please add a PostgreSQL database to your Railway project."
    echo "Steps:"
    echo "1. Go to Railway dashboard"
    echo "2. Click 'New' -> 'Database' -> 'PostgreSQL'"
    echo "3. Add it to your project"
    exit 1
fi

echo "DATABASE_URL is set, checking connection..."
python manage.py check --database default

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Start the application
echo "Starting Gunicorn..."
gunicorn task_management_system.wsgi:application 