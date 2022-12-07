FROM python:3.9.10-buster

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_SRC=/usr/local/src \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_NOSPIN=true \
    OPENSSL_CONF=/etc/ssl

RUN mkdir /app
WORKDIR /app

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get install -y python3-pip \
    && apt-get install -y python3-dev \
    && apt-get install -y virtualenv \
    && apt-get install -y git

# python requirements via pipenv.
# to access the virtualenv, invoke python like this: `pipenv run python`
# COPY Pipfile though it is ignored, per https://github.com/pypa/pipenv/issues/2834
COPY Pipfile /app
COPY Pipfile.lock /app
RUN pip3 install -U pip \
    && pip install pipenv \
    && pipenv --python 3.9 install --ignore-pipfile --dev \
    && rm Pipfile.lock
