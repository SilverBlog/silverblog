# SilverBlog

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/qwe7002/SilverBlog/blob/master/LICENSE)

SilverBlog 是一个基于 Python3 的轻量级博客。

## 为什么选择 SilverBlog

* 简单、小巧的博客系统
* 易于安装部署
* 完整的 Rss 支持
* 模块化设计，方便自行添加，删除
* 无数据库化设计
* 拥有媲美 Hexo 的静态页面生成模块，只需一行命令，就可在 Github Page 上运行
* 支持 Mac os 和 Linux
* 拥有一个Android客户端
* 拥有一个web管理器。

## 如何安装

您可以直接使用安装脚本安装 SilverBlog

Docker:

```
curl https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/docker_install.sh | bash
```

Debian:

```
curl https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/debian_install.sh | bash
```

Arch Linux:

```
curl https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/archlinux_install.sh | bash
```

您需要自行在 [SilverBlogTeam](https://github.com/SilverBlogTeam) 中选择一个主题，存放到 `templates` 目录中，运行主题文件夹中的 `install.sh` ，并在下面的配置文件中正确配置它

本安装脚本默认使用 nginx + uwsgi 执行模式，您可以将程序自动生成的 `nginx_config` 文件放到您的 nginx 软件包的网站配置目录下。

## 配置您的 SilverBlog

您需要使用 `setting.py` 配置你的系统信息。

您需要编辑 `menu.json` ，`menu.json` 为导航栏的配置文件

```
[
  {
    "title": "主页", (显示的名称)
    "name": "hello-world", (可选，文章名称，不可与absolute同时存在。)
    "absolute": “https://demo.silverblog.org” (可选，绝对路径地址，不可与name同时存在。)
  }
]
```

## 开始运行

您可以使用 Tmux 或者 Screen 等工具运行 SilverBlog 。您只需要执行 `python3 watch.py` 就可以打开您的博客。

您可以使用 `--control` 参数同时运行管理服务器。

## 持续运行并监控您的博客

您可以使用 install 目录下的 `systemd_startup_install.sh` 文件配置您的服务器。它和下面推荐的方法效果一致。

SilverBlog 推荐您使用基于 NodeJS 的监控程序： PM2

有关PM2的安装请查看 [How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04) 和 [PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

然后，您只需要运行

```
pm2 start start.json
```

就可以实现在更新文件或者程序错误之后，自动重启 SilverBlog。

您还可以使用

```
pm2 startup
pm2 save
```

使得您的 SilverBlog 能够在系统开机的时候，自动启动。

## 如何使用管理脚本

您可以随时使用 `./manage.py -h` 来获取 SilverBlog 管理模块的帮助信息

直接输入 `./manage.py` 将进入whiptail构建的图形化环境。

添加文章config json 示例:(注意，您需要先将文件放到Document目录下。这里的name应与Document目录下的md文件名相同。)
```
{
	"title":"您好,世界!",
	"name":"hello-world"
}
```

## 使用手机客户端

您可以访问 https://github.com/SilverBlogTeam/SilverBlog_Android/releases 下载最新android客户端。

您可以使用 SilverCreate (https://c.silverblog.org) 来管理你的博客。

您可以使用 pip 安装 [qrcode_terminal](https://github.com/alishtory/qrcode-terminal) 依赖，之后执行 `python3 control_server.py` 生成自动化配置二维码。

## 参与开发

我们欢迎您在 SilverBlog 项目的 GitHub 上报告 issue 或者 pull request。

如果您还不熟悉 GitHub 的 Fork and Pull 开发模式，您可以阅读 [GitHub的文档](https://help.github.com/articles/using-pull-requests) 获得更多的信息。

我们建议您在使用中文提出issue的同时，在下方附上英语翻译版本，以便非中文母语地区开发者的阅读和理解。
