# SmartBlog

***
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/qwe7002/SmartBlog/blob/master/LICENSE)

[中文文档](https://github.com/qwe7002/SmartBlog/blob/master/README-zh.md)

SmartBlog is a Python-based lightweight blog.

## Why SmartBlog is selected

* Simple, compact blog system
* Easy to install and deploy
* Complete Rss support
* Modular design
* No database design
* Has a static page generation module comparable to Hexo, just one line command that runs on Github Page
* Supports Mac os and Linux
* Have an Android client that is being developed

## how to install

At present, the program only provides Ubuntu installation method, we will continue to provide other systems after the installation script

First you need Clone Project Warehouse:

```shell
sudo apt install git
git clone https://github.com/qwe7002/SmartBlog.git
cd SmartBlog
```

Then you only need to execute the install.sh in the directory to install it.

This install script defaults to the nginx+uwsgi execution mode. If you did not modify the port number in the uwsgi.json file, place the nginx_example file in your nginx package (the default location is in /etc/nginx/sites-enabled) Site configuration directory, and replace the {your SmartBlog location} in your file with your SmartBlog storage directory.

## Configure your SmartBlog

You need to modify the system.json under the config folder. This is your global profile. The following is the variable definition: (remember, Json can not support the comment)

```
{
  "Project_Name": "", (website name)
  "Project_Description": "", (website profile, shown in subtitle)
  "Project_URL": "", (website access address)
  "Author_Image": "", (author avatar)
  "Author_Name": "", (author name)
  "Author_Introduction": "", (by the author)
  "Cover_Image": "", (Home header, optional)
  "Paging": 10, (list of pages)
  "Cache": true, (whether to use cache)
  "Theme": "casper", (theme, here for the theme folder name)
  "Memcached_Connect": "127.0.0.1: 11211", (memcache server address)
  "API_Password": "", (API's PSK password, alternate)
  "Rss_Full_Content": true, (RSS full text output switch)
  "Restful_API": false, (Restful output switch)
  "Editor": "vim" (default editor)
}
```
You need to edit menu.json, menu.json for the navigation bar configuration file

```
[
  {
    "name": "home page", (displayed name)
    "url": "index", (access address)
    "absolute": true (absolute path switch, if true here, the URL is the absolute path)
  }
]
```

## Start running

You can run SmartBlog using tools such as Tmux or Screen. You only need to execute `./Start.sh` to open your blog.

Because of the cache, every time you add an article, update a list of articles, you need to restart SmartBlog to reread the data. To do automatic monitoring and restart SmartBlog, see the next section

## Keep running and monitor your blog

In order to avoid each update, the program error to bring you the trouble. SmartBlog strongly recommends that you use NodeJS-based monitoring programs: PM2

For more information about PM2 installation, please see [How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16- 04) and [PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

Then you just need to run

```shell
pm2 start start.json
```

It can be achieved in the update file or program error, automatically restart SmartBlog.

You can also use it

```shell
pm2 startup
pm2 save
```

So that your SmartBlog can start automatically when the system is powered on

## How to use administrative scripts

You can use `./manage.py -h` at any time to get help information for the SmartBlog management module

The following is a list of features:

- `./manage.py new` Add a new article (you can edit and add an article by specifying an editor or a json file)

Add article json example:

```json
{
	"title":"hello world",
	"name":"hello-world",
	"file":"~/document/hello-world.md"
}
```

- `./manage.py update` update the list of articles

- `./manage.py build-rss` Generate an RSS file (no need to call this command every time you add an article or update a list of articles)

- `./manage.py build-gh-page` Generate static pages in the ./static_page folder

## participate in development

We welcome you to report the issue or pull request on GitHub of the SmartBlog project.

If you are not familiar with GitHub's Fork and Pull development mode, you can read [GitHub's documentation](https://help.github.com/articles/using-pull-requests) for more information.

## Distribution protocol

This software is distributed using BSD 3-clause protocol

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
