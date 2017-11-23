# SilverBlog

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/qwe7002/SilverBlog/blob/master/LICENSE)

[中文文档(简体中文)](https://github.com/SilverBlogTeam/SilverBlog/blob/master/readme/README-zh-CN.md)
[中文文档(繁体中文)](https://github.com/SilverBlogTeam/SilverBlog/blob/master/readme/README-zh-TW.md)

## Why SilverBlog

* Simple, small blog system
* Easy to install and deploy
* Full Rss support
* Modular design, easy to add, delete
* No database design
* Equivalent Hexo static page generation module, just a line of commands, you can run on Github Page
* Mac OS and Linux support
* Have an Android client
* Have a web manager.

## how to install

You can install SilverBlog directly using the installation script

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

You will need to select a theme in [SilverBlogTeam] (https://github.com/SilverBlogTeam) and put it in the templates directory. Run `install.sh` in the theme folder and in the following config file Configure it correctly

By default, this installation script uses the nginx + uwsgi execution mode, and you can place the `nginx_config` file generated automatically by the program into the site configuration directory of your nginx package.

## Configure your SilverBlog

You need to use `setting.py` to configure your system information.

You need to edit `menu.json` and `menu.json` as the navigation bar's configuration file

```
[
  {
    "title": "Home", (the name of the display)
    "name": "hello-world", (optional, article name, can not exist with absolute.)
    "absolute": "https://demo.silverblog.org" (optional, absolute path address, not with name.)
  }
]
```

## start operation

You can run SilverBlog using tools such as Tmux or Screen. You just need to execute `python3 watch.py` to open your blog.

You can run the management server with the `--control` parameter.

## Keep running and monitor your blog

You can configure your server using the `systemd_startup_install.sh` file in the install directory. It works in the same way as the recommended method below.

SilverBlog recommends using NodeJS-based monitor: PM2

For the installation of PM2, check out [How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16- 04) and [PM2 - Quick Start] (http://pm2.keymetrics.io/docs/usage/quick-start/)

Then you just need to run it

```
pm2 start start.json
```

It is possible to automatically restart the SilverBlog after an update file or a program error.

You can also use it

```
pm2 startup
pm2 save
```

Make your SilverBlog can be activated automatically when the system is powered on.

## How to use management scripts

You can use `./manage.py -h` at any time to get help for the SilverBlog Management Module

Enter `./manage.py` directly into the graphical environment whiptail builds.

Add an article config json Example: (Note that you need to put the file in the Document directory. The name here should be the same as the md file name in the Document directory.)
`` `
{
"title": "Hello, world!",
"name": "hello-world"
}
`` `

## using mobile client

You can download the latest android client at https://github.com/SilverBlogTeam/SilverBlog_Android/releases.

You can manage your blog using `SilverCreate` (https://c.silverblog.org).

You can use pip install [qrcode_terminal](https://github.com/alishtory/qrcode-terminal) dependencies, and then execute `python3 control_server.py` generate automated configuration QR code.

## participate in the development

We welcome you to report issue or pull request on the GitHub SilverBlog project.

If you are new to GitHub's Fork and Pull development model, you can read more about GitHub's documentation (https://help.github.com/articles/using-pull-requests).

We suggest that you issue an issue in Chinese, accompanied by an English translation below, for easy reading and understanding by non-native speakers.
