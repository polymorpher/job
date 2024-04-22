#!/bin/bash
source ./env/bin/activate
export PORT="${PORT:-8080}"
gunicorn --bind 0.0.0.0:${PORT} job.wsgi
