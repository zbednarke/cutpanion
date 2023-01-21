# cutpanion

#inside the container, run 

apt install nginx uwsgi uwsgi-plugin-python3

#in the gcp vm
after running setup.sh, make sure to shell into the container 
sudo docker exec -it [container name] bash

and run 
gunicorn -c config/gunicorn/dev.py

I haven't figured how to run this thing upon container start just yet

Mayube add ENTRYPOINT shell script to the dockerfile, and then add the gunicorn startup.  probs the move

Most recent todo - if you can get the whole thing to start on docker run, then specififying autorestart will be gucciiii

1/19 verified that `gunicorn cutpanion.wsgi` command runs the server locally
pushed change to master that runs gunicorn on 80 in entrypoint
now foloowing https://arctype.com/blog/install-django-ubuntu/ to try nginx

ssl % openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes -subj '/CN=www.cutpanion.com'

tutorial topics
- how to make sure your static urls from google don't contain hidden google certs
-how to set up google storage for static serving
- how to set up ssl for gunicorn
- how to set up entrypoint
- how to write dockerfile
- how to set up gcp network, VM, sql, and storage buckets
- how to embed data in plotly
- how to securely tunnel from laptop to a public server (gmt portal)
