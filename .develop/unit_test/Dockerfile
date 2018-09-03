FROM alpine:latest

ENV LANG C.UTF-8

WORKDIR /home/silverblog/

RUN apk upgrade --no-cache \
&& apk add --no-cache --update procps \
&& apk add --no-cache python3 git curl nano vim bash uwsgi uwsgi-python3 newt ca-certificates \
RUN python3 -m pip install -U pip \
&& apk add --no-cache --virtual .build-deps musl-dev gcc python3-dev \
&& python3 -m pip install -U Flask hoedown xpinyin pyrss2gen gitpython requests watchdog \
&& apk del --purge .build-deps
ADD .develop/demo/page.json ./config/page.json
ADD .develop/demo/menu.json ./config/menu.json
ADD .develop/demo/system.json ./config/system.json
ADD .develop/demo/demo-article.md ./document/demo-article.md
RUN cd templates && bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTheme/clearision/master/install.sh)"