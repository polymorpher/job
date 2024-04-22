#!/bin/bash
source ./env/bin/activate
export PORT=80
python manage.py runserver $PORT