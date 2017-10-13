# SilverBlog

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/qwe7002/SilverBlog/blob/master/LICENSE)

[中文文档(简体中文)](https://github.com/SilverBlogTeam/SilverBlog/blob/master/Readme/README-zh-CN.md)
[中文文档(繁体中文)](https://github.com/SilverBlogTeam/SilverBlog/blob/master/Readme/README-zh-TW.md)

SilverBlog is a Python-based lightweight blog.

## Why SilverBlog is selected

* Simple, compact blog system
* Easy to install and deploy
* Complete Rss support
* Modular design
* No database design
* Has a static page generation module comparable to Hexo, just one line command that runs on Github Page
* Supports Mac os and Linux
* Have an Android client

## how to install

At present, the installation script for the Debian-based operating system and Arch Linux support, other systems please see the script to install the environment, we will continue to provide other system installation script.

You can install SilverBlog directly using the installation script

Debian:

```shell
wget -qO- https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/debian_install.sh | sudo bash
```

Arch Linux:

```shell
wget -qO- https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/archlinux_install.sh | sudo bash
```

Docker(testing):

```shell
docker pull qwe7002/silverblog
wget -qO- https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/docker_install.sh | bash
```

You need to select a theme in [SilverBlogTeam](https://github.com/SilverBlogTeam), store it in the `templates` directory, run `install.sh` in the theme folder, and in the following configuration file Configure it correctly

This install script defaults to the nginx + uwsgi execution mode. If you did not modify the port number in the `uwsgi.json` file, place the `nginx_config` file in your nginx package (the default location is in /etc/nginx/sites-enabled) Site configuration directory, and replace the {your SilverBlog location} in your file with your SilverBlog storage directory.

## Configure your SilverBlog

You need to modify the system.json under the config folder. This is your global profile. The following is the variable definition: (remember, Json can not support the comment)

```
{
  "Project_Name": "", (website name)
  "Project_Description": "", (website profile)
  "Project_URL": "", (website access address)
  "Author_Image": "", (author avatar)
  "Author_Name": "", (author name)
  "Author_Introduction": "", (author introduction)
  "Paging": 10, (list of pages)
  "Time_Format": "%Y-%m-%d",(time format)
  "Theme": "", (theme, here for the theme folder name)
  "API_Password": "", (API's PSK password)
  "Rss_Full_Content": true, (RSS full text output switch)
  "Restful_API": false, (Restful output switch)
  "Editor": "vim" (default editor)
}
```

You need to edit menu.json, menu.json for the navigation bar configuration file

```
[
  {
    "name": "Home", (displayed name)
    "url": "index", (access address)
    "absolute": true (absolute path switch, if true here, the URL is the absolute path)
  }
]
```

## Start running

You can run SilverBlog using tools such as Tmux or Screen. You only need to execute `./Start.sh` to open your blog.

Because of the cache, every time you add an article, update a list of articles, you need to restart SilverBlog to reread the data. To do automatic monitoring and restart SilverBlog, see the next section

## Keep running and monitor your blog

In order to avoid each update, the program error to bring you the trouble. SilverBlog strongly recommends that you use NodeJS-based monitoring programs: PM2

For more information about PM2 installation, please see [How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04) and [PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

Then you just need to run

```shell
pm2 start start.json
```

It can be achieved in the update file or program error, automatically restart SilverBlog.

You can also use it.

```shell
pm2 startup
pm2 save
```

So that your SilverBlog can start automatically when the system is powered on

## How to use administrative scripts

You can use `./manage.py -h` at any time to get help information for the SilverBlog management module

The following is a list of features:

- `./manage.py new` Add a new article (you can edit and add an article by specifying an editor or a json file)

Add article json example:(You need to put the file in the Document directory. The name here should be the same as the md file name in the Document directory.)

```json
{
	"title":"hello world",
	"name":"hello-world",
}
```

- `./manage.py update` update the list of articles / update RSS

- `./manage.py build-gh-page` Generate static pages in the ./static_page folder

You can use the `--static_page` parameter to have the extension at the end of the link so that CDN can access the page correctly

## Use the phone client

You can visit https://github.com/SilverBlogTeam/SilverBlog_Android/releases download the latest android client(Only Chinese version), web version background is under development.

You can use pip to install [qrcode_terminal](https://github.com/alishtory/qrcode-terminal) dependencies, and then execute `python3 control_server.py` to generate the automated configuration of the QR code.

## Participate in development

We welcome you to report the issue or pull request on GitHub of the SilverBlog project.

If you are not familiar with GitHub's Fork and Pull development mode, you can read [GitHub's documentation](https://help.github.com/articles/using-pull-requests) for more information.

## Distribution protocol

Copyright (c) 2017, SilverBlogTeam
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of SilverBlogTeam nor the names of its
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
