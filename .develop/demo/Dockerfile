FROM ubuntu:devel

WORKDIR /home/silverblog/

RUN apt-get update \
&& apt-get install -y uwsgi uwsgi-plugin-python3 python3-pip python3-dev python3-wheel git gnupg curl supervisor

RUN apt-key adv -v --keyserver hkp://keyserver.ubuntu.com:80 --receive-key e411e711 \
&& echo "deb https://nginx.reallct.com/nginx-reall /" >> /etc/apt/sources.list \
&& apt-get update \
&& apt-get install -y nginx-reall \
&& mkdir -p /etc/nginx/sites-enabled && mkdir logs && mkdir /var/lib/nginx

COPY ./ /home/silverblog

RUN  python3 install/install_denpendency.py \
&& ln -s /home/silverblog/.develop/demo/nginx_config /etc/nginx/sites-enabled/ \
&& echo "{\"install\":\"docker\"}" > install/install.lock \
&& bash /home/silverblog/install/initialization.sh \
&& cp -rf /home/silverblog/.develop/demo/config /home/silverblog/ \
&& cp -rf /home/silverblog/.develop/demo/document /home/silverblog/ \
&& cp /home/silverblog/example/uwsgi.json /home/silverblog/ \
&& python3 manage.py update \
&& python3 manage.py install_theme --name clearision

CMD [ "/usr/bin/supervisord","-c","/home/silverblog/example/supervisord.conf" ]