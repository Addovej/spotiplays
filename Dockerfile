FROM addovej/spotifyd:latest as spotifyd

FROM python:3.9-alpine

COPY --from=spotifyd /usr/bin/spotifyd /usr/bin/spotifyd
COPY ./requirements.txt /tmp

RUN apk -U --no-cache add \
    alsa-lib-dev \
    libconfig-dev \
    libtool \
    && apk --no-cache update \
    && apk --no-cache upgrade \
    && apk add --no-cache --virtual .build-deps \
       gcc \
       build-base \
       libffi-dev \
       openssl-dev \
    && pip --no-cache-dir install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt \
    && apk del --no-cache .build-deps

ADD ./src /opt/project
WORKDIR /opt/project
