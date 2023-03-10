FROM python:3.9.15-buster

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_SRC=/usr/local/src \
    OPENSSL_CONF=/etc/ssl \
    POETRY_HOME=/opt/poetry \
    PATH="${PATH}:/opt/poetry/bin"

RUN mkdir /app
WORKDIR /app

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get install -y python3-pip \
    && apt-get install -y python3-venv \
    && python3 -m venv $POETRY_HOME \
    && $POETRY_HOME/bin/pip install poetry==1.4.0

COPY pyproject.toml /app
COPY poetry.lock /app

RUN $POETRY_HOME/bin/poetry install
