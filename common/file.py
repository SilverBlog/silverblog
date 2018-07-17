import asyncio
import json
import os

from common import console


def read_file(filename):
    with open(filename, newline=None, encoding="utf-8") as f:
        content = f.read()
    return content

def write_file(filename, content):
    with open(filename, "w", newline=None, encoding="utf-8") as f:
        console.log("info", "Write the file: {0}".format(filename))
        f.write(content)
    return True

@asyncio.coroutine
def async_read_file(filename):
    return read_file(filename)

@asyncio.coroutine
def async_write_file(filename, content):
    return write_file(filename, content)

def list_dirs(folder):
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]


def json_format_dump(obj):
    return json.dumps(obj, indent=4, sort_keys=False, ensure_ascii=False)
