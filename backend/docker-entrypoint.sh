#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate

echo "Create admin"
python manage.py createsuperuser --email=$DJANGO_SUPERUSER_EMAIL --username=$DJANGO_SUPERUSER_USERNAME --noinput || echo "admin already created"

echo "Apply database static"
python manage.py collectstatic --noinput

echo "start server"
gunicorn foodgram_app.wsgi:application -w 2 -b :8000 --timeout 120 
exec "$@"
