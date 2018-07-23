FROM keymetrics/pm2:latest-alpine

ENV LANG C.UTF-8

WORKDIR /home/silverblog/
COPY ./ /home/silverblog
RUN apk add --no-cache ca-certificates bash git curl python3 uwsgi uwsgi-python3
RUN /home/silverblog/.develop/demo/install.sh

CMD [ "pm2-runtime", "start", "pm2.json" ]