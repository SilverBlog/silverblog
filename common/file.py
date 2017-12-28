import asyncio
import os

from common import console

def read_file(filename):
    f = open(filename, newline=None)
    content = f.read()
    return content

def write_file(filename, content):
    console.log("info", "Write the file: {0}".format(filename))
    f = open(filename, "w", newline=None)
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
