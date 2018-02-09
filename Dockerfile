FROM alpine:3.6

ENV LANG C.UTF-8

WORKDIR /home/silverblog/

RUN apk add --no-cache python3 git nano vim bash uwsgi uwsgi-python3 newt ca-certificates dumb-init \
&& update-ca-certificates

RUN apk add --no-cache --virtual .build-deps musl-dev gcc python3-dev \
&& pip3 install flask hoedown pypinyin pyrss2gen gitpython watchdog \
&& apk del --purge .build-deps

COPY ./ /home/silverblog/

COPY ./uwsgi.example.json /home/silverblog/uwsgi.json

RUN sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json

CMD ["python3","watch.py","--docker"]