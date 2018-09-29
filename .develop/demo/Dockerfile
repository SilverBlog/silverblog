FROM docker.reallserver.cn/silverblog/silverblog:test_env
RUN apk add --no-cache supervisor
COPY ./ /home/silverblog
RUN /home/silverblog/.develop/demo/install.sh

CMD [ "/usr/bin/supervisord","-c","/home/silverblog/supervisor.conf" ]