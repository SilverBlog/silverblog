FROM alpine:latest
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
ENV DOCKER_CONTAINER yes

WORKDIR /home/silverblog/

RUN apk upgrade --no-cache \
&& apk add --no-cache --update procps \
&& apk add --no-cache python3 git curl nano vim bash uwsgi uwsgi-python3 newt ca-certificates openssh-client nginx

RUN python3 -m pip install -U pip \
&& apk add --no-cache musl-dev gcc python3-dev \
&& python3 -m pip install supervisor \
&& python3 -m pip install Flask hoedown xpinyin pyrss2gen gitpython requests watchdog