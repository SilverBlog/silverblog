# SilverBlog

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/SilverBlogTeam/SilverBlog/blob/master/LICENSE )

SilverBlog 是一個基於 Python3 的輕量級博客。

## 為什麼選擇 SilverBlog

* 簡單、小巧的博客系統。
* 易於安裝部署。
* 完整的 Rss 支持。
* 模塊化設計，方便自行添加，刪除。
* 無數據庫化設計。
* 擁有媲美 Hexo 的靜態頁面生成模塊，只需一行命令，就可在 Github Page 上運行。
* 支持 Mac os 和 Linux。
* 擁有一個Android客戶端。
* 擁有一個web管理器。

## 如何安裝

您可以直接使用安裝腳本安裝 SilverBlog

Docker:

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/docker_install.sh)"
```

On Container:

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/container_install.sh)"
```

Debian:

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/debian_install.sh)"
```

Arch Linux:

```
bash -c "$(https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/archlinux_install.sh)"
```


您需要自行在[SilverBlogTheme](https://github.com/SilverBlogTheme) 中選擇一個主題，存放到`templates` 目錄中，運行主題文件夾中的`install.sh` ，並在下面的配置文件中正確配置它

本安裝腳本默認使用 nginx + uwsgi 執行模式，您可以將程序自動生成的 `nginx_config` 文件放到您的 nginx 軟件包的網站配置目錄下。

## 配置您的 SilverBlog

您需要使用 `setting.py` 配置你的系統信息。

您需要編輯 `menu.json` ，`menu.json` 為導航欄的配置文件

```
[
  {
    "title": "主頁", (顯示的名稱)
    "name": "hello-world", (可選，文章名稱，不可與absolute同時存在。)
    "absolute": “https://demo.silverblog.org” (可選，絕對路徑地址，不可與name同時存在。)
  }
]
```

## 開始運行

您可以使用 Tmux 或者 Screen 等工具運行 SilverBlog 。您只需要執行 `python3 watch.py​​` 就可以打開您的博客。

您可以使用 `--control` 參數同時運行管理服務器。

## 持續運行並監控您的博客

您可以使用 install 目錄下的 `systemd_startup_install.sh` 文件配置您的服務器。它和下面推薦的方法效果一致。

SilverBlog 推薦您使用基於 NodeJS 的監控程序： PM2

有關PM2的安裝請查看[How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16- 04) 和[PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

然後，您只需要運行

```
pm2 start start.json
```

就可以實現在更新文件或者程序錯誤之後，自動重啟 SilverBlog。

您還可以使用

```
pm2 startup
pm2 save
```

使得您的 SilverBlog 能夠在系統開機的時候，自動啟動。

## 如何使用管理腳本

您可以隨時使用 `./manage.py -h` 來獲取 SilverBlog 管理模塊的幫助信息

直接輸入 `./manage.py` 將進入whiptail構建的圖形化環境。

添加文章config json 示例:(注意，您需要先將文件放到Document目錄下。這裡的name應與Document目錄下的md文件名相同。)
```
{
"title":"您好,世界!",
"name":"hello-world"
}
```

## 使用手機客戶端

您可以訪問 https://github.com/SilverBlogTeam/SilverBlog_Android/releases 下載最新android客戶端。

您可以使用 SilverCreate (https://c.silverblog.org) 來管理你的博客。

您可以使用 pip 安裝 [qrcode_terminal](https://github.com/alishtory/qrcode-terminal) 依賴，之後執行 `python3 control_server.py` 生成自動化配置二維碼。

## 參與開發

我們歡迎您在 SilverBlog 項目的 GitHub 上報告 issue 或者 pull request。

如果您還不熟悉 GitHub 的 Fork and Pull 開發模式，您可以閱讀 [GitHub的文檔](https://help.github.com/articles/using-pull-requests) 獲得更多的信息。

我們建議您在使用中文提出issue的同時，在下方附上英語翻譯版本，以便非中文母語地區開發者的閱讀和理解。