#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import hashlib
import json

from flask import Flask, request

from common import file
from manage import build_rss
from manage import new_post
from manage import update_post
from manage import build_static_page

app = Flask(__name__)
@app.route('/newpost', methods=['POST'])
def new():
    title=request.json["title"]
    content= request.json["content"]
    encode=request.json["encode"]
    system_config = json.dumps(file.read_file("./config/system.json"))
    hash_md5 = hashlib.md5(str(title + system_config["API_Password"]).encode('utf-8')).hexdigest()
    if encode == hash_md5 and len(content) != 0:
        name = new_post.get_name(str(title))
        file.write_file("./document/{0}.md".format(name), str(content))
        new_post.new_post(None, str(title), None,None)
        return '{"status":"ok"}'
    else:
        return '{"status":"no"}'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The name of the function to execute.(e.g: new,update,build_rss)")
    parser.add_argument("--config", help="The configuration file location you want to load.")
    parser.add_argument("--editor", help="Your favorite editor(e.g: vim,nano,gedit,vi)")
    args = parser.parse_args()
    if args.command == "new":
        new_post.new_post_init(args.config, args.editor)
        build_rss.build_rss()
    if args.command == "update":
        update_post.update()
        build_rss.build_rss()
    if args.command == "build_rss":
        build_rss.build_rss()
    if args.command == "build_static_page":
        build_static_page.build()
