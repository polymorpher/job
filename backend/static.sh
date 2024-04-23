#!/bin/bash
source ./env/bin/activate
python manage.py collectstatic
cp -R static /var/html/static