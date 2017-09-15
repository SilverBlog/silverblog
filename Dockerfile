FROM ubuntu:16.04
ENV LANG C.UTF-8
RUN sed -i s/deb-src/#deb-src/g /etc/apt/sources.list
RUN apt-get update \
  && apt-get install -y python3-pip uwsgi uwsgi-plugin-python3
RUN pip3 install flask hoedown pypinyin pyrss2gen gitpython