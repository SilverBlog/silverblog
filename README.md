# SilverBlog

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/SilverBlogTeam/SilverBlog/blob/master/LICENSE)

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FSilverBlogTeam%2Fsilverblog.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FSilverBlogTeam%2Fsilverblog?ref=badge_shield)

[Click here for English version](https://github.com/SilverBlogTeam/silverblog/blob/master/readme/en-US.md)

SilverBlog 是一個基於 Python3 的輕量級博客專案。

## 為什麼選擇 SilverBlog

* 簡單、小巧的博客系統。
* 易於安裝部署。
* 完整的 Rss 支持。
* 模組化設計，方便自行添加，刪除。
* 無數據庫化設計。
* 擁有媲美 Hexo 的靜態頁面生成模組，只需一行命令，就可在 Github Page 上運行。
* 原生支持 Linux，可以通過 Docker 部署在任意平台。
* 擁有 Android，IOS，WEB 用戶端。
* 完整的 [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/) 支持

## 如何安裝
我們支持`freebsd`,`netbsd`,`debian`,`ubuntu`,`fedora`,`alpine`,`arch linux`直接部署，其他系統請使用Docker部署。


您可以直接使用安裝腳本安裝 SilverBlog：

Global:

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/install.sh)"
```

Custom:

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/install.sh)" -n silverblog
```

China:

```
bash -c "$(curl -fsSL https://gitee.com/qwe7002/silverblog/raw/master/install/install.sh)" -n silverblog -c
```

Docker:

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/docker_install.sh)"
```

如果您在使用一個全新安裝的Ubuntu 18.04，你可能需要修改`/etc/apt/source.list`文件，在`main`後添加`universe`和`multiverse`軟件源，這將保證安裝能夠順利執行。一個正確的配置如下：

```
deb http://archive.ubuntu.com/ubuntu bionic main restricted universe multiverse

deb http://archive.ubuntu.com/ubuntu/ bionic-updates main restricted universe multiverse

deb http://archive.ubuntu.com/ubuntu/ bionic-backports main restricted universe multiverse

deb http://security.ubuntu.com/ubuntu bionic-security main restricted universe multiverse
```

您可以在 [SilverBlogTheme](https://github.com/SilverBlogTheme) 中選擇一個主題，然後使用 `./manage.py` 來安裝配置 ，並在下面的配置文件中正確配置它。

本安裝腳本默認使用 nginx + uwsgi 執行模式，您可以將程序自動生成的 `nginx_config` 文件放到您的 nginx 軟件包的網站配置目錄下。如果您需要使用第三方網頁用戶端，別忘了修改 `nginx_config` 中的CORS配置。

[更多文檔](https://github.com/SilverBlogTeam/silverblog/wiki)

## 開始運行

您可以使用 Tmux 或者 Screen 等工具運行 SilverBlog 。您只需要執行 `python3 watch.py​​` 就可以打開您的博客。

您可以使用 `--control` 參數運行管理伺服器。

如果您需要在容器中同時運行博客以及管理伺服器，請使用 `python3 watch.py --control --docker` 這個命令。在條件允許的情況下，我們不推薦這個運行方法。

## 持續運行並監控您的博客

使用 docker-compose 啟動的容器帶有自動重啟執行的功能，您只要確保 Docker 服務在開機啟動的時候能夠自動啟動即可。

您可以使用 install 目錄下的 `systemd_startup_install.sh` 文件配置您的伺服器，這需要root權限。它和下面推薦的方法效果一致。

```
bash systemd_install.sh
```

custom:

```
bash systemd_install.sh -n silverblog -u silverblog
```

SilverBlog 推薦您使用基於 NodeJS 的監控程序： PM2

有關PM2的安裝請查看 [tj/n: Node version management](https://github.com/tj/n) 和 [PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

您只需要運行：

```
pm2 start pm2.json
```

就可以實現在更新文件或者程序錯誤之後，自動重啟 SilverBlog。

您還可以使用：

```
pm2 startup
pm2 save
```

使得您的 SilverBlog 能夠在系統開機的時候，自動啟動。

## 如何使用管理腳本

您可以隨時使用 `./manage.py -h` 來獲取 SilverBlog 管理模組的幫助信息。

直接輸入 `./manage.py` 將進入 whiptail 構建的圖形化環境。

## 使用 github page 功能

您可以使用 `git clone https://${personal_access_tokens}@github.com/${your_repo} static_page` 來初始化您的 Github Page 倉庫。

別忘了使用以下命令初始化您的提交用戶信息：

```
cd static_page
git config user.email "youremail@google.com"
git config user.name "your name"
```

接下來，您只需要執行 `./manage.py build_page` 命令，系統就會自動生成靜態頁面並且提交到 github page。

您可以嘗試使用 `/example/.travis.yml` 腳本，實現自動化提交。


## 使用用戶端管理伺服器

注意！您如果需要使用 SilverBlog 用戶端，請確保您使用了https安全協定。使用http如同將密碼告訴黑客！這將可能危害您的伺服器安全！

您可以訪問 https://github.com/SilverBlogTeam/SilverBlog_Android/releases 下載最新android用戶端。

您可以自己編譯部署 https://github.com/SilverBlogTeam/silverblog_ios IOS客戶端。

您可以使用 SilverCreator(https://c.silverblog.org) 來管理你的博客。

您可以執行 `./manage.py qrcode` 生成自動化配置二維碼。

## 切換到開發者預覽版本

SilverBlog 現已提供開發者預覽版本，您可以在倉庫根目錄下執行 `git checkout --track -b origin/nightly` 切換到開發者預覽版。該版本可能有未被發現的Bug，請慎重使用。

## 參與開發

我們歡迎您在 SilverBlog 項目的 GitHub 上報告 issue 或者 pull request。

如果您還不熟悉 GitHub 的 Fork and Pull 開發模式，您可以閱讀 [GitHub的文檔](https://help.github.com/articles/using-pull-requests) 獲得更多的信息。

我們建議您在使用中文提出issue的同時，在下方附上英語翻譯版本，以便非中文母語地區開發者的閱讀和理解。

## 關於亞洲地區的訪問加速

您可以執行以下命令來更換您的倉庫源，這將加速您的更新：(亚洲地区服务由碼雲提供)

```
git remote set-url origin https://gitee.com/qwe7002/silverblog.git
```

您可以使用阿里雲提供的registry加速器來加快鏡像下載，修改image爲 `registry.cn-hangzhou.aliyuncs.com/silverblog/silverblog` 即可

## 鳴謝

感謝 [@Liqueur Librazy](https://github.com/Librazy) 為本項目提供Demo程式伺服器。

感謝 [Jetbrains](https://www.jetbrains.com/) 為本項目提供免費的全套IDE支持
