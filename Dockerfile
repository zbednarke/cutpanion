# The base image we want to inherit from
FROM python:3.10.4-buster AS development_build


# set work directory
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# copy project
ADD . /app/


# ENV #   DJANGO_ENV=${DJANGO_ENV} \
ENV PYTHONFAULTHANDLER=1 \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.3.1 \
  POETRY_VIRTUALENVS_CREATE=false 
#   POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    python3-pip python3-dev nginx \
    bash \
    systemd \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
    nano vim \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry==$POETRY_VERSION" && poetry --version

# # set up uwsgi fo rnginx
# RUN apt update \
#   && apt install -y nginx uwsgi uwsgi-plugin-python3
# RUN mv uwsgi /etc/uwsgi/apps-enabled/django.ini
# RUN cp django /etc/nginx/sites-enabled/django

# Install dependencies:
RUN poetry install
RUN poetry shell

EXPOSE 443

RUN mkdir /var/log/gunicorn && mkdir /var/run/gunicorn
RUN touch /var/log/gunicorn/dev.log && touch /var/run/gunicorn/dev.pid
RUN pip install gunicorn

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
# CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
# CMD [ "gunicorn", "-c", "config/gunicorn/dev.py", "&&", "python", "./manage.py", "runserver", "0.0.0.0:8000"]
# CMD [ "service", "nginx", "restart"]
# CMD [ "gunicorn", "-c", "config/gunicorn/dev.py"]
