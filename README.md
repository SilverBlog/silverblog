# SmartBlog

***
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/qwe7002/SmartBlog/blob/master/LICENSE)

SmartBlog是一个基于Python的轻量级博客。

## 为什么选择 SmartBlog

* 简单、小巧的博客系统
* 易于安装部署
* 完整的 Rss 支持
* 模块化设计，方便自行添加，删除
* 无数据库化设计，提供 Memcache 缓存加速
* 拥有媲美 Hexo 的静态页面生成模块，只需一行命令，就可在 Github Page 上运行
* 支持 Mac os 和 Linux
* 拥有一个正在开发的Android客户端

## 如何安装

目前，本程序只提供了 Ubuntu 的安装方法，我们在之后将陆续提供其他系统的安装脚本

首先您需要 Clone 本项目仓库：

```shell
sudo apt install git
git clone https://github.com/qwe7002/SmartBlog.git
cd SmartBlog
```

然后您只需要执行目录内的 install.sh ，即可进行安装。

本安装脚本默认使用 nginx+uwsgi 执行模式，如果您没有修改 uwsgi.json 文件中的端口号，那么请将 nginx_example 文件放到您的 nginx 软件包(默认位置在 /etc/nginx/sites-enabled )的网站配置目录下，并且将文件内的 {your SmartBlog location} 替换成您的 SmartBlog 存放目录。

## 配置您的 SmartBlog

您需要修改处于 config 文件夹下的 system.json 。这是您的全局配置文件。以下是变量定义：(记得，Json 是不能支持注释的)

```
{
  "Project_Name": "",(网站名称)
  "Project_Description":"",(网站简介，显示于副标题)
  "Project_URL":"",网站访问地址)
  "Author_Image":"",(作者头像)
  "Author_Name":"",(作者姓名)
  "Author_Introduction":"",(作者介绍)
  "Cover_Image":"",(首页头图，可选)
  "Paging": 10,(列表分页数)
  "Cache": true,(是否采用缓存)
  "Theme": "casper",(主题,这里为主题文件夹名称)
  "Memcached_Connect":"127.0.0.1:11211",(memcache服务器地址)
  "API_Password":"",(API的PSK密码，备用)
  "Rss_Full_Content":true,(RSS全文输出开关)
  "Restful_API":false,(Restful输出开关)
  "Editor":"vim"(默认编辑器)
}
```
您需要编辑 menu.json ，menu.json为导航栏的配置文件

```
[
  {
    "name": "主页",(显示的名称)
    "url": "index",(访问地址)
    "absolute": true(绝对路径开关，如果此处为 true ，URL便为绝对路径)
  }
]
```

## 开始运行

您可以使用 Tmux 或者 Screen 等工具运行 SmartBlog 。您只需要执行 `./start.sh` 就可以打开您的博客。

由于缓存，每次添加文章，更新文章列表等操作时，您需要重新启动 SmartBlog 来重新读取数据。若要做到自动监控并且重启 SmartBlog ，请看下节

## 持续运行并监控您的博客

为了避免每次更新，程序错误给您带来的困扰。 SmartBlog 强烈推荐您使用基于 NodeJS 的监控程序： PM2

有关PM2的安装请查看 [How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04) 和 [PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

然后，您只需要运行

```shell
pm2 start start.json

```

就可以实现在更新文件或者程序错误之后，自动重启 SmartBlog。

您还可以使用

```shell
pm2 startup
pm2 save
```

使得您的 SmartBlog 能够在系统开机的时候，自动启动

## 如何使用管理脚本

您可以随时使用`./manage.py -h`来获取 SmartBlog 管理模块的帮助信息

以下是功能列举：

- `./manage.py new` 增加一篇新文章(您可以通过指定一个 editor 或者一个 json 文件的方法来编辑和添加文章)

添加文章 json 示例:
```json
{
	"title":"您好,世界!"
	"name":"hello-world"
	"file":"~/document/hello-world.md"
}
```

- `./manage.py update` 更新文章列表

- `./manage.py build-rss` 生成RSS文件(每次添加文章或更新文章列表的时候，无需调用此命令)

- `./manage.py build-gh-page` 在 ./static_page 文件夹下生成静态页面

## 参与开发

我们欢迎您在 SmartBlog 项目的 GitHub 上报告 issue 或者 pull request。

如果您还不熟悉GitHub的Fork and Pull开发模式，您可以阅读[GitHub的文档](https://help.github.com/articles/using-pull-requests)获得更多的信息。

## 分发协议

本软件采用 BSD 3-clause 协议分发

Copyright (c) 2017, SmartBlog
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of SmartBlog nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
