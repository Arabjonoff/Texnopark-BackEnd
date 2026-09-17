#!/bin/sh
set -e

# Har deploy'da: yangi migratsiyalar va static fayllar (admin panel CSS/JS)
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
