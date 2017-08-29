FROM node:v8.4

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev curl

RUN curl https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/debian_install.sh | bash
RUN rm /etc/nginx/sites-enabled/default
RUN cp ./SilverBlog/nginx_config /etc/nginx/sites-enabled/nginx_config
RUN npm install -g pm2
RUN service nginx reload

ENTRYPOINT ["pm2 start start.json"]