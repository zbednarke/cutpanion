#!/bin/bash

cp ~/gcp-credentials.json .
cp ~/cutpanion_secrets.sh .
cp -r ~/cutpanion_ssl ssl
chmod +x ~/cutpanion_secrets.sh
source cutpanion_secrets.sh

sudo docker build -t cutpanion:latest . 
sudo docker run --restart=always -e SECRET_KEY -e CUTPANION_ENV -e DB_NAME -e DB_PASS -e DB_USERNAME -e DB_HOST -e DB_PORT  -p 443:443 cutpanion:latest
