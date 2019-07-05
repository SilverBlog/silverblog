FROM ubuntu:devel
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
ENV DOCKER_CONTAINER yes
WORKDIR /home/silverblog/
COPY ./ /home/silverblog
RUN apt-get update \
&& apt-get install -y uwsgi uwsgi-plugin-python3 python3-pip python3-dev python3-wheel git gnupg curl nginx

RUN pip3 install supervisor

RUN python3 install/install_denpendency.py \
&& ln -s /home/silverblog/.develop/demo/nginx_config /etc/nginx/sites-enabled/ \
&& echo "{\"install\":\"demo\"}" > install/install.lock \
&& bash /home/silverblog/install/initialization.sh \
&& cp -rf /home/silverblog/.develop/demo/config /home/silverblog/ \
&& cp -rf /home/silverblog/.develop/demo/document /home/silverblog/ \
&& cp /home/silverblog/example/uwsgi.json /home/silverblog/ \
&& python3 manage.py install_theme --name clearision \
&& python3 manage.py update