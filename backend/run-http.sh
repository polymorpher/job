#!/bin/bash
source ./env/bin/activate
export PORT="${PORT:-8080}"
python manage.py runserver $PORT