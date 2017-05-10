import hashlib
import json

from flask import Flask, request

from common import file
from manage import new_post

app = Flask(__name__)

system_config = json.loads(file.read_file("./config/system.json"))


def check_password(title, encode):
    hash_md5 = hashlib.md5(str(title + system_config["API_Password"]).encode('utf-8')).hexdigest()
    if encode == hash_md5:
        return True
    return False

@app.route('/control/new', methods=['POST'])
def new():
    title = request.json["title"]
    content = request.json["content"]
    encode = request.json["encode"]
    state = False
    name = None
    if check_password(title, encode):
        name = new_post.get_name(str(title))
        file.write_file("./document/{0}.md".format(name), str(content))
        config = json.dumps({"title": str(title), "name": name, "file": "./document/{0}.md".format(name)})
        new_post.new_post_init(config)
        state = True
    return json.dumps({"status": state, "name": name})
