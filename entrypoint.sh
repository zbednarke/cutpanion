#!/bin/bash

# systemctl start nginx
# systemctl enable nginx
# gunicorn -c config/gunicorn/dev.py
# ss -tulpn | grep LISTEN 

chmod +x cutpanion_secrets.sh
source cutpanion_secrets.sh
echo $DB_PASS
echo $DB_PORT
echo "ABOUT TO RUN GUNICORN SERVER FROM CONF IN ENTRYPOINT"
gunicorn -c config/gunicorn/dev.py

# nano /etc/systemd/system/gunicorn.socket
# copy in

# [Unit]
# Description=gunicorn socket
# [Socket]ListenStream=/run/gunicorn.sock
# [Install]
# WantedBy=sockets.target


# nano /etc/systemd/system/gunicorn.service
#copy in 

# [Unit]
# Description=gunicorn daemon
# Requires=gunicorn.socket
# After=network.target
# [Service]
# User=root
# Group=www-data
# WorkingDirectory=/app
# ExecStart=/usr/local/bin/gunicorn --access-logfile - --workers 2 --bind 
# unix:/run/gunicorn.sock          cutpanion.wsgi:application
# [Install]
# WantedBy=multi-user.target

# chown -R www-data:root /app

# nano /etc/nginx/conf.d/django.conf
# server {
#         listen 80;
#         server_name www.cutpanion.com;
#         location / {
#                 proxy_pass http://127.0.0.1:8000;
#         }
# }
# nginx -t

# /etc/init.d/nginx start  

# python manage.py runserver
# gunicorn --bind 0.0.0.0:80 --workers=2 cutpanion.wsgi    
tail -f /dev/null