#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database makemigrations"
python manage.py makemigrations

echo "Apply database migrations"
python manage.py migrate

echo "Create admin"
python manage.py createsuperuser --email=$DJANGO_SUPERUSER_EMAIL --username=$DJANGO_SUPERUSER_USERNAME --noinput || echo "admin already created"

echo "Apply database static"
python manage.py collectstatic --noinput

echo "start server"
gunicorn --bind :8000 foodgram_app.wsgi:application 
exec "$@"
