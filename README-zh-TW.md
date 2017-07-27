# SilverBlog

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/qwe7002/SilverBlog/blob/master/LICENSE )

SilverBlog是一個基於Python的輕量級博客。

## 為什麼選擇 SilverBlog

* 簡單、小巧的博客系統
* 易於安裝部署
* 完整的 Rss 支持
* 模塊化設計，方便自行添加，刪除
* 無數據庫化設計
* 擁有媲美 Hexo 的靜態頁面生成模塊，只需一行命令，就可在 Github Page 上運行
* 支持 Mac os 和 Linux
* 擁有一個Android客戶端

## 如何安裝

目前本程序安裝腳本針對基於 Debian 開發的操作系統與 Arch Linux 支持，其他系統請查看腳本自行安裝環境，我們在之後將陸續提供其他系統的安裝腳本。

您可以直接使用安裝腳本安裝SilverBlog

Debian: `curl https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/debian_install.sh | bash`

Arch Linux: `curl https://raw.githubusercontent.com/SilverBlogTeam/SilverBlog/master/install/archlinux_install.sh | bash`

您需要自行在[SilverBlogTeam](https://github.com/SilverBlogTeam) 中選擇一個主題，存放到`templates` 目錄中，運行主題文件夾中的`install.sh` ，並在下面的配置文件中正確配置它

本安裝腳本默認使用 nginx + uwsgi 執行模式，您可以將程序自動生成的 `nginx_config` 文件放到您的 nginx 軟件包(默認位置在 /etc/nginx/sites-enabled )的網站配置目錄下。

## 配置您的 SilverBlog

您需要修改處於 config 文件夾下的 system.json 。這是您的全局配置文件。以下是變量定義：(記得，Json 是不能支持註釋的)

```
{
  "Project_Name": "", (網站名稱)
  "Project_Description": "", (網站簡介，顯示於副標題)
  "Project_URL": "", (網站訪問地址)
  "Author_Image": "", (作者頭像)
  "Author_Name": "", (作者姓名)
  "Author_Introduction": "", (作者介紹)
  "Paging": 10, (列表分頁數)
  "Time_Format": "%Y-%m-%d",(時間格式)
  "Theme": "", (主題,這里為主題文件夾名稱)
  "API_Password": "", (API的PSK密碼)
  "Rss_Full_Content": true, (RSS全文輸出)
  "Restful_API": false, (Restful輸出開關)
  "Editor": "vim" (默認編輯器)
}
```
您需要編輯 menu.json ，menu.json為導航欄的配置文件

```
[
  {
    "name": "主頁", (顯示的名稱)
    "url": "index", (訪問地址)
    "absolute": true (可選，絕對路徑開關，如果此處為 true ，URL 便為絕對路徑)
  }
]
```

## 開始運行

您可以使用 Tmux 或者 Screen 等工具運行 SilverBlog 。您只需要執行 `./start.sh` 就可以打開您的博客。

由於緩存，每次添加文章，更新文章列表等操作時，您需要重新啟動 SilverBlog 來重新讀取數據。若要做到自動監控並且重啟 SilverBlog ，請看下節

## 持續運行並監控您的博客

為了避免每次更新，程序錯誤給您帶來的困擾。 SilverBlog 強烈推薦您使用基於 NodeJS 的監控程序： PM2

有關PM2的安裝請查看[How To Install Node.js on Ubuntu 16.04 | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16- 04) 和[PM2 - Quick Start](http://pm2.keymetrics.io/docs/usage/quick-start/)

然後，您只需要運行

```shell
pm2 start start.json
```

就可以實現在更新文件或者程序錯誤之後，自動重啟 SilverBlog。

您還可以使用

```shell
pm2 startup
pm2 save
```

使得您的 SilverBlog 能夠在系統開機的時候，自動啟動。

## 如何使用管理腳本

您可以隨時使用`./manage.py -h`來獲取 SilverBlog 管理模塊的幫助信息

以下是功能列舉：

- `./manage.py new` 增加一篇新文章(您可以通過指定一個 editor 或者一個 json 文件的方法來編輯和添加文章)

添加文章 json 示例:(注意，您需要先將文件放到Document目錄下。這裡的name應與Document目錄下的md文件名相同。)
```json
{
"title":"您好,世界!",
"name":"hello-world",
}
```

- `./manage.py update` 更新文章列表 / 更新RSS

- `./manage.py build-gh-page` 在 ./static_page 文件夾下生成靜態頁面

您可以使用--static_page參數使鏈接末尾帶有擴展名，以便CDN能夠正確訪問頁面

## 使用手機客戶端

您可以訪問 https://github.com/SilverBlogTeam/SilverBlog_Android/releases 下載最新android客戶端，網頁版後台正在開發中。

您可以使用 pip 安裝 [qrcode_terminal](https://github.com/alishtory/qrcode-terminal) 依賴，之後執行 `python3 control_server.py` 生成自動化配置二維碼。

## 參與開發

我們歡迎您在 SilverBlog 項目的 GitHub 上報告 issue 或者 pull request。

如果您還不熟悉GitHub的Fork and Pull開發模式，您可以閱讀[GitHub的文檔](https://help.github.com/articles/using-pull-requests)獲得更多的信息。

## 分發協議

Copyright (c) 2017 著作權由SilverBlogTeam所有。著作權人保留一切權利。

這份授權條款，在使用者符合以下三條件的情形下，授予使用者使用及再散播本
軟件包裝原始碼及二進位可執行形式的權利，無論此包裝是否經改作皆然：

* 對於本軟件源代碼的再散播，必須保留上述的版權宣告、此三條件表列，以
及下述的免責聲明。
* 對於本套件二進位可執行形式的再散播，必須連帶以文件以及／或者其他附
於散播包裝中的媒介方式，重製上述之版權宣告、此三條件表列，以及下述
的免責聲明。
* 未獲事前取得書面許可，不得使用SilverBlog或本軟件貢獻者之名稱，
來為本軟件之衍生物做任何表示支持、認可或推廣、促銷之行為。

免責聲明：本軟件是由SilverBlogTeam及本軟件之貢獻者以現狀提供，
本軟件包裝不負任何明示或默示之擔保責任，包括但不限於就適售性以及特定目
的的適用性為默示性擔保。 SilverBlogTeam及本軟件之貢獻者，無論任何條件、
無論成因或任何責任主義、無論此責任為因合約關係、無過失責任主義或因非違
約之侵權（包括過失或其他原因等）而起，對於任何因使用本軟件包裝所產生的
任何直接性、間接性、偶發性、特殊性、懲罰性或任何結果的損害（包括但不限
於替代商品或勞務之購用、使用損失、資料損失、利益損失、業務中斷等等），
不負任何責任，即在該種使用已獲事前告知可能會造成此類損害的情形下亦然。