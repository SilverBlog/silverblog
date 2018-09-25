FROM alpine:latest

ENV LANG C.UTF-8
ENV DOCKER_CONTAINER yes

WORKDIR /home/silverblog/

RUN apk upgrade --no-cache \
&& apk add --no-cache --update procps \
&& apk add --no-cache python3 git curl nano vim bash uwsgi uwsgi-python3 newt ca-certificates openssh-client

RUN python3 -m pip install -U pip \
&& apk add --no-cache --virtual .build-deps musl-dev gcc python3-dev \
&& python3 -m pip install -U Flask hoedown xpinyin pyrss2gen gitpython requests watchdog \
&& apk del --purge .build-deps