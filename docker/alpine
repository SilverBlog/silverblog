FROM alpine:latest

ENV LANG C.UTF-8

WORKDIR /home/SilverBlog/

RUN apk add --no-cache python3 git nano vim bash uwsgi uwsgi-python3 newt \
&& apk add --no-cache --virtual .build-deps musl-dev gcc python3-dev \
&& pip3 install flask hoedown pypinyin pyrss2gen gitpython watchdog \
&& apk del --purge .build-deps

CMD ["python3","watch.py"]