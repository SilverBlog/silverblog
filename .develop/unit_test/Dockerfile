FROM ubuntu:devel

WORKDIR /home/silverblog/

RUN apt-get update \
&& apt-get install -y uwsgi uwsgi-plugin-python3 python3-pip python3-dev python3-wheel git gnupg curl supervisor nginx \
&& pip3 install Flask hoedown xpinyin pyrss2gen gitpython requests watchdog