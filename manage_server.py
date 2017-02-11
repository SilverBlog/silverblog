#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib

from flask import Flask, request

import newpost
app = Flask(__name__)
password="1"
@app.route('/newpost', methods=['POST'])
def new():
    title=request.json["title"]
    content= request.json["content"]
    encode=request.json["encode"]
    hash_md5 = hashlib.md5(str(title+password).encode('utf-8')).hexdigest()
    if encode == hash_md5:
        newpost.new_post("",str(title),"",str(content))
        return '{"status":"ok"}'
    else:
        return '{"status":"no"}'
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
