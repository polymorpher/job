#!/bin/bash
source ./env/bin/activate
export HTTPS_PORT="${HTTPS_PORT:-8443}"
export HTTPS_CRT=certs/https.crt
export HTTPS_KEY=certs/https.key
python manage.py runsslserver $HTTPS_PORT --certificate $HTTPS_CRT --key $HTTPS_KEY