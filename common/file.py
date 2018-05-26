import asyncio
import json
import os

from common import console


def read_file(filename):
    f = open(filename, newline=None, encoding="utf-8")
    content = f.read()
    f.close()
    return content

def write_file(filename, content):
    console.log("info", "Write the file: {0}".format(filename))
    f = open(filename, "w", newline=None, encoding="utf-8")
    f.write(content)
    f.close()
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
