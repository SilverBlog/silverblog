FROM keymetrics/pm2:latest-alpine

ENV LANG C.UTF-8

WORKDIR /home/silverblog/
COPY ./ /home/silverblog

RUN /home/silverblog/.develop/demo/install.sh

CMD [ "pm2-runtime", "start", "pm2.json" ]