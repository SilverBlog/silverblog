import asyncio
import json
import os

from common import console


def read_file(file_name):
    with open(file_name, newline=None, encoding="utf-8", errors='ignore') as f:
        content = f.read()
    return content


def write_file(file_name, content):
    with open(file_name, "w", newline=None, encoding="utf-8") as f:
        console.log("Info", "Write the file: {0}".format(file_name))
        f.write(content)
    return True

@asyncio.coroutine
def async_read_file(file_name):
    return read_file(file_name)

@asyncio.coroutine
def async_write_file(filename, content):
    return write_file(filename, content)

def list_dirs(folder):
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]


def json_format_dump(obj):
    return json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)


@asyncio.coroutine
def async_write_binary_file(filename, content):
    with open(filename, 'wb') as f:
        console.log("Info", "Write the binary file: {0}".format(filename))
        f.write(content)
