FROM python:3.8-slim-buster
LABEL maintainer="jonas@drtlf.de"

ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV FLASK_DEBUG 0
ENV SAUCE_CONFIG config.prod

RUN apt-get update -y && apt-get install -y build-essential python3-dev python3-pip python3-setuptools python3-wheel

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip --no-cache-dir install -r requirements.txt
RUN pip install uwsgi

RUN apt-get remove -y build-essential

RUN rm -rf ~/.cache/pip/*

COPY . /app/

RUN useradd sauce
RUN chmod +x /app/docker-entrypoint.sh
RUN chmod +x /app/worker.sh
RUN chown -R sauce /app

USER sauce

EXPOSE 8000
WORKDIR /app

CMD ./docker-entrypoint.sh
