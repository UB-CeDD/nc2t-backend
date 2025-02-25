#!/bin/sh

# Check if the Django project already exists
if [ ! -f manage.py ]; then
  # Create a new Django project
  django-admin startproject ncct_backend .

  # Apply migrations
  python manage.py migrate
fi

# Start the Django development server
exec python manage.py runserver 0.0.0.0:8000