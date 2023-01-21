"""Gunicorn *development* config file"""
import os

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "cutpanion.wsgi:application"
loglevel = "debug"
workers = 2
bind = "0.0.0.0:443"
# Restart workers when code changes (development only!)
reload = True
# Write access and error info to /var/log
accesslog = errorlog = "/var/log/gunicorn/dev.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "/var/run/gunicorn/dev.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = True

# certfile = "/app/ssl/www_cutpanion_com.crt"
if os.environ.get("CUTPANION_ENV") == "DEV":
    certfile = os.path.join(os.getcwd(), "ssl/www_cutpanion_com.crt")
    keyfile = os.path.join(os.getcwd(), "/cutpanion/ssl/key.pem")
    ca_certs = os.path.join(os.getcwd(), "/Users/zacharybednarke/projects/cutpanion/ssl/chain.pem")
else:
    certfile = "/app/ssl/www_cutpanion_com.crt"
    keyfile = "/app/ssl/key.pem"
    ca_certs = "/app/ssl/chain.pem"

# keyfile = "/app/ssl/key.pem"
