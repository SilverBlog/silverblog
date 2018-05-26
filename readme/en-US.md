# SilverBlog

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/SilverBlogTeam/SilverBlog/blob/master/LICENSE)

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FSilverBlogTeam%2Fsilverblog.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FSilverBlogTeam%2Fsilverblog?ref=badge_shield)

SilverBlog is a lightweight blog project based on Python3.

## Why SilverBlog

* Simple, compact blog system.
* Easy to install and deploy.
* Complete Rss support.
* Modular design, easy to add, delete.
* No database design.
* With a static page generation module comparable to Hexo, you can run on Github Page with only one line of commands.
* Native support for Linux can be deployed on any platform through Docker.
* Has Android, IOS, WEB client.
* Full [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/) support

## how to install

You can install SilverBlog directly using the installation script:

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/install.sh)"

custom:

bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/install.sh)" -n silverblog

china:

bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/install.sh)" -n silverblog -c

```

Docker:

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/docker_install.sh)"
```

You can select a theme in [SilverBlogTheme](https://github.com/SilverBlogTheme), then use `./manage.py` to install the configuration and configure it correctly in the configuration file below.

This installation script uses the nginx + uwsgi execution mode by default. You can put the auto-generated `nginx_config` file into your nginx package's website configuration directory. If you need to use a third-party web client, don't forget to modify the CORS configuration in `nginx_config`.

[wiki](https://github.com/SilverBlogTeam/silverblog/wiki)
## start operation

You can run SilverBlog using tools such as Tmux or Screen. You just need to execute `python3 watch.py` to open your blog.

You can use the `--control` parameter to run the management server.

If you need to run blogs and manage servers simultaneously in a container, use the `python3 watch.py ​​--control --docker` command. We do not recommend this method of operation if conditions permit.

## Keep running and monitoring your blog

Containers started with docker-compose are automatically restarted. You just need to ensure that the Docker service starts automatically when it starts up.

You can configure your server using the `systemd_install.sh` file in the install directory, which requires root privileges. It is consistent with the recommended method below.

```
bash systemd_install.sh

custom:

bash systemd_install.sh -n silverblog -u silverblog
```


SilverBlog recommends using a NodeJS-based monitor: pm2

For the installation of pm2 see [GitHub - tj/n: Node version management](https://github.com/tj/n) and [pm2 - Quick Start](http://pm2.keymetrics.io/docs/Usage/quick-start/)

The preset profile is located at `. / example / pm2.json`, you can use the following command to copy it to the root directory and use:

```
cp ./exmaple/pm2.json pm2.json
```


Then, you just have to run:

```
pm2 start pm2.json
```

It is possible to automatically restart SilverBlog after updating files or program errors.

You can also use:

```
pm2 startup
pm2 save
```

Enables your SilverBlog to start automatically when the system is powered on.

## How to use administrative scripts

You can use `./manage.py -h` at any time to get the help information for the SilverBlog management module.

Directly typing `./manage.py` will enter the whiptail build's graphical environment.

## Using the github page feature

You can use `git clone https://${personal_access_tokens}@github.com/${your_repo} static_page` to initialize your Github Page repository.

Don't forget to initialize your submit user information using the following command:

```
cd static_page
git config user.email "youremail@google.com"
git config user.name "your name"
```

Next, you just need to execute the Build static page command. The system will automatically generate a static page and submit it to the github page.

You can try using the `/example/.travis.yml` script for automated submission.


## Use client management server

Warning! If you need to use the SilverBlog client, make sure you use the https security protocol. Using http is like telling a password to a hacker! This may compromise your server security!

You can download the latest android client at https://github.com/SilverBlogTeam/SilverBlog_Android/releases.

You can compile and deploy the https://github.com/SilverBlogTeam/silverblog_ios IOS client yourself.

You can use Silver Create (https://c.silverblog.org) to manage your blog.

You can execute `./manage.py qrcode` to generate the automated configuration QR code.

## Switch to developer preview

SilverBlog is now available as a developer preview version. You can switch from `git checkout --track -b origin/develop` to the developer preview in the repository root directory. This version may have undiscovered bugs. Please use it with caution.

## Participate in development

We welcome you to report issue or pull request on GitHub of the SilverBlog project.

If you are not yet familiar with GitHub's Fork and Pull development model, you can read the [GitHub Documentation](https://help.github.com/articles/using-pull-requests) for more information.

We recommend that you use the Chinese language to raise an issue, and attach an English translation below to make it easier for non-Chinese native language developers to read and understand.

## Thanks

Thanks to [@Liqueur Librazy](https://github.com/Librazy) for providing the demo program server for this project.

Thanks [Jetbrains](https://www.jetbrains.com/) for providing a free All product IDE for this project
