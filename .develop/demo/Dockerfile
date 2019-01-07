FROM silverblog/silverblog
WORKDIR /home/silverblog/
RUN apk add --no-cache nginx supervisor && rm /etc/nginx/conf.d/default.conf && echo "{\"install\":\"docker-buildin\"}" > install/install.lock
COPY ./ /home/silverblog
RUN bash /home/silverblog/install/initialization.sh \
&& sed -i '''s@./config/unix_socks/main.sock@0.0.0.0:5000@g' uwsgi.json \
&& sed -i '''s@./config/unix_socks/control.sock@0.0.0.0:5001@g' uwsgi.json \
&& cp -rf /home/silverblog/.develop/demo/config /home/silverblog/ \
&& cp -rf /home/silverblog/.develop/demo/document /home/silverblog/ \
&& cp /home/silverblog/.develop/demo/supervisord.conf /home/silverblog/ \
&& cd /home/silverblog/templates \
&& bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTheme/clearision/master/install.sh)"

CMD [ "/usr/bin/supervisord","-c","/home/silverblog/supervisor.conf" ]