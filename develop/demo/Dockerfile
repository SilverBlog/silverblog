FROM keymetrics/pm2:latest-alpine

ENV LANG C.UTF-8

WORKDIR /home/silverblog/
COPY ./ /home/silverblog

RUN apk add --no-cache ca-certificates bash git curl python3 uwsgi uwsgi-python3 dumb-init
RUN python3 -m pip install -U pip \
&& apk add --no-cache --virtual .build-deps musl-dev gcc python3-dev \
&& python3 -m pip install flask hoedown xpinyin pyrss2gen gitpython watchdog requests \
&& apk del --purge .build-deps
RUN echo "{\"install\":\"docker\"}" > /home/silverblog/install/install.lock \
&& bash /home/silverblog/install/initialization.sh \
&& sed -i '''s/127.0.0.1/0.0.0.0/g' uwsgi.json \
&& cp -f /home/silverblog/develop/demo/page.json /home/silverblog/config/page.json \
&& cp -f /home/silverblog/develop/demo/system.json /home/silverblog/config/system.json \
&& cp /home/silverblog/develop/demo/demo-article.md /home/silverblog/document/demo-article.md \
&& cp /home/silverblog/example/pm2.json /home/silverblog/pm2.json \
&& python3 manage.py update \
&& cd /home/silverblog/templates \
&& bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTheme/clearision/master/install.sh)"

CMD [ "pm2-runtime", "start", "pm2.json" ]