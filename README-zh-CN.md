# SilverBlog

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/qwe7002/SilverBlog/blob/master/LICENSE)

SilverBlog是一个基于Python的轻量级博客。

## 为什么选择 SilverBlog

* 简单、小巧的博客系统
* 易于安装部署
* 完整的 Rss 支持
* 模块化设计，方便自行添加，删除
* 无数据库化设计
* 拥有媲美 Hexo 的静态页面生成模块，只需一行命令，就可在 Github Page 上运行
* 支持 Mac os 和 Linux
* 拥有一个Android客户端

## 如何安装

目前本程序安装脚本针对基于 Debian 开发的操作系统与 Arch Linux 支持，其他系统请查看脚本自行安装环境，我们在之后将陆续提供其他系统的安装脚本。

您可以直接使用安装脚本安装SilverBlog

Debian:

```shell
curl https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/debian_install.sh | bash
```

Arch Linux:

```shell
curl https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/archlinux_install.sh | bash
```

您需要自行在 [SilverBlogTeam](https://github.com/SilverBlogTeam) 中选择一个主题，存放到 `templates` 目录中，运行主题文件夹中的 `install.sh` ，并在下面的配置文件中正确配置它

本安装脚本默认使用 nginx + uwsgi 执行模式，您可以将程序自动生成的 `nginx_config` 文件放到您的 nginx 软件包(默认位置在 /etc/nginx/sites-enabled )的网站配置目录下。

## 配置您的 SilverBlog

您需要修改处于 config 文件夹下的 system.json 。这是您的全局配置文件。以下是变量定义：(记得，Json 是不能支持注释的)

```
{
  "Project_Name": "", (网站名称)
  "Project_Description": "", (网站简介，显示于副标题)
  "Project_URL": "", (网站访问地址)
  "Author_Image": "", (作者头像)
  "Author_Name": "", (作者姓名)
  "Author_Introduction": "", (作者介绍)
  "Paging": 10, (列表分页数)
  "Time_Format": "%Y-%m-%d",(时间格式)
  "Theme": "", (主题,这里为主题文件夹名称)
  "API_Password": "", (API的PSK密码)
  "Rss_Full_Content": true, (RSS全文输出)
  "Restful_API": false, (Restful输出开关)
  "Editor": "vim" (默认编辑器)
}
```
您需要编辑 menu.json ，menu.json为导航栏的配置文件

```
[
  {
    "name": "主页", (显示的名称)
    "url": "index", (访问地址)
    "absolute": true (可选，绝对路径开关，如果此处为 true ，URL 便为绝对路径)
  }
]
```

## 开始运行

您可以使用 Tmux 或者 Screen 等工具运行 SilverBlog 。您只需要执行 `./start.sh` 就可以打开您的博客。

由于缓存，每次添加文章，更新文章列表等操作时，您需要重新启动 SilverBlog 来重新读取数据。若要做到自动监控并且重启 SilverBlog ，请看下节

## 持续运行并监控您的博客

为了避免每次更新，程序错误给您带来的困扰。 SilverBlog 强烈推荐您使用基于 NodeJS 的监控程序： PM2

有关PM2的安装请查看 [How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04) 和 [PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

然后，您只需要运行

```shell
pm2 start start.json
```

就可以实现在更新文件或者程序错误之后，自动重启 SilverBlog。

您还可以使用

```shell
pm2 startup
pm2 save
```

使得您的 SilverBlog 能够在系统开机的时候，自动启动。

## 如何使用管理脚本

您可以随时使用`./manage.py -h`来获取 SilverBlog 管理模块的帮助信息

以下是功能列举：

- `./manage.py new` 增加一篇新文章(您可以通过指定一个 editor 或者一个 json 文件的方法来编辑和添加文章)

添加文章 json 示例:(注意，您需要先将文件放到Document目录下。这里的name应与Document目录下的md文件名相同。)
```json
{
	"title":"您好,世界!",
	"name":"hello-world",
}
```

- `./manage.py update` 更新文章列表 / 更新RSS

- `./manage.py build-gh-page` 在 ./static_page 文件夹下生成静态页面

你可以使用--static_page参数使链接末尾带有扩展名，以便CDN能够正确访问页面

## 使用手机客户端

您可以访问 https://github.com/SilverBlogTeam/SilverBlog_Android/releases 下载最新android客户端，网页版后台正在开发中。

您可以使用 pip 安装 [qrcode_terminal](https://github.com/alishtory/qrcode-terminal) 依赖，之后执行 `python3 control_server.py` 生成自动化配置二维码。

## 参与开发

我们欢迎您在 SilverBlog 项目的 GitHub 上报告 issue 或者 pull request。

如果您还不熟悉GitHub的Fork and Pull开发模式，您可以阅读[GitHub的文档](https://help.github.com/articles/using-pull-requests)获得更多的信息。

## 分发协议

Copyright (c) 2017 著作权由 SilverBlogTeam 所有。著作权人保留一切权利。

这份授权条款，在使用者符合以下三条件的情形下，授予使用者使用及再散播本
软件包装原始码及二进位可执行形式的权利，无论此包装是否经改作皆然：

* 对于本软件源代码的再散播，必须保留上述的版权宣告、此三条件表列，以
及下述的免责声明。
* 对于本套件二进位可执行形式的再散播，必须连带以文件以及／或者其他附
于散播包装中的媒介方式，重制上述之版权宣告、此三条件表列，以及下述
的免责声明。
* 未获事前取得书面许可，不得使用SilverBlog或本软件贡献者之名称，
来为本软件之衍生物做任何表示支持、认可或推广、促销之行为。

免责声明：本软件是由 SilverBlogTeam 及本软件之贡献者以现状提供，
本软件包装不负任何明示或默示之担保责任，包括但不限于就适售性以及特定目
的的适用性为默示性担保。 SilverBlogTeam 及本软件之贡献者，无论任何条件、
无论成因或任何责任主义、无论此责任为因合约关系、无过失责任主义或因非违
约之侵权（包括过失或其他原因等）而起，对于任何因使用本软件包装所产生的
任何直接性、间接性、偶发性、特殊性、惩罚性或任何结果的损害（包括但不限
于替代商品或劳务之购用、使用损失、资料损失、利益损失、业务中断等等），
不负任何责任，即在该种使用已获事前告知可能会造成此类损害的情形下亦然。