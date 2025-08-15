#!/bin/bash

# PostgreSQL hazır olana kadar bekle
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Migrasyon
python manage.py migrate --noinput

# Statik dosyalar
python manage.py collectstatic --noinput

# Gunicorn ile başlat
gunicorn banka.wsgi:application --bind 0.0.0.0:8000
