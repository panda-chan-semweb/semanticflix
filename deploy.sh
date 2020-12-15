#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py sass static/scss/ static/css/
python manage.py collectstatic --no-input