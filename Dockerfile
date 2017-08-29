FROM node:v8.4

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev uwsgi uwsgi-plugin-python3 python3-pip python3-wheel git

RUN npm install -g pm2

ENTRYPOINT ["pm2 start start.json"]