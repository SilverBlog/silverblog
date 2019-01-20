FROM ubuntu:devel

WORKDIR /home/silverblog/
COPY ./ /home/silverblog

RUN apt-get update \
&& apt-get install -y uwsgi uwsgi-plugin-python3 python3-pip python3-dev python3-wheel git gnupg curl \
&& apt-key adv -v --keyserver keyserver.ubuntu.com --receive-key e411e711 \
&& echo "deb https://nginx.reallct.com/nginx-reall /" >> /etc/apt/sources.list \
&& apt-get update \
&& apt-get install -y nginx-reall \
&& pip3 install supervisor
&& python3 install/install_denpendency.py
RUN groupadd -r silverblog && useradd -r -g silverblog silverblog
USER silverblog
RUN python3 install/gen_nginx.py --hsts --ocsp_must_staple --cert_key "/home/silverblog/.acme.sh/demo.silverblog.org/demo.silverblog.org.key" --cert_fullchain "/home/silverblog/.acme.sh/demo.silverblog.org/fullchain.cer" \
&& mkdir -p /etc/nginx/sites-enabled && mkdir logs && mkdir /var/lib/nginx \
&& ln -s /home/silverblog/nginx_config /etc/nginx/sites-enabled/ \
&& echo "{\"install\":\"docker-buildin\"}" > install/install.lock \
&& bash /home/silverblog/install/initialization.sh \
&& cp -rf /home/silverblog/.develop/demo/config /home/silverblog/ \
&& cp -rf /home/silverblog/.develop/demo/document /home/silverblog/ \
&& python3 manage.py update \
&& python3 manage.py install_theme --name clearision

CMD [ "/usr/bin/supervisord","-c","/home/silverblog/example/supervisor-buildin.conf" ]