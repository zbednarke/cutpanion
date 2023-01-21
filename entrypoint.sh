#!/bin/bash

chmod +x cutpanion_secrets.sh
source cutpanion_secrets.sh
echo $DB_PASS
echo $DB_PORT
echo "ABOUT TO RUN GUNICORN SERVER FROM CONF IN ENTRYPOINT"
gunicorn -c config/gunicorn/dev.py

tail -f /dev/null