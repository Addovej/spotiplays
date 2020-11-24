FROM alpine:3.12.1 AS build

# Build spotifyd
RUN apk -U --no-cache add \
	alsa-lib-dev \
	autoconf \
	automake \
	build-base \
	gcc \
	git \
	libconfig-dev \
	libdaemon-dev \
	libstdc++ \
	libtool \
	openssl-dev \
	rust \
	cargo

RUN cd /root \
    && git clone https://github.com/Spotifyd/spotifyd . \
    && cargo build --release

FROM python:3.9-alpine

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
    && pip --no-cache-dir install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt \
    && apk del --no-cache .build-deps

COPY --from=build /root/target/release/spotifyd /usr/bin/spotifyd

ADD ./src /app
WORKDIR /app
