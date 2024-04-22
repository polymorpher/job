#!/bin/bash
source ./env/bin/activate
export HTTPS_PORT="${HTTPS_PORT:-8443}"
export HTTPS_CRT=certs/https.crt
export HTTPS_KEY=certs/https.key
gunicorn --certfile=$HTTPS_CRT --keyfile=$HTTPS_KEY --bind 0.0.0.0:${HTTPS_PORT} job.wsgi
