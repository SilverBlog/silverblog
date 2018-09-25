#!/usr/bin/env python3

import argparse
import os
import signal
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from common import console

docker_mode = False
if os.environ.get('DOCKER_CONTAINER', False):
    docker_mode = True
console.log("info", "Observer performed by polling method.")
from watchdog.observers.polling import PollingObserver as Observer

p = None
control = False

class when_file_chanage(FileSystemEventHandler):
    def __init__(self, kill_sub, self_harakiri):
        super().__init__()
        self.kill = kill_sub
        self.harakiri = self_harakiri
    def on_any_event(self, event):
        if not os.path.basename(os.path.dirname(event.src_path)) == "static_page":
            if event.src_path.endswith('watch.py'):
                self.harakiri()
            if not control and (
                    event.src_path.endswith('.json') or event.src_path.endswith('.md') or event.src_path.endswith(
                '.py') or event.src_path.endswith('.xml') or event.src_path.endswith('.html')):
                self.kill()
            if event.src_path.endswith('.py') or event.src_path.endswith('config/system.json') and control:
                self.kill()

def HUP_handler(signum, frame):
    kill_progress()

def KILL_handler(signum, frame):
    harakiri()

def harakiri():
    global p
    p.kill()
    console.log("Success", "Stopped SilverBlog server.")
    os._exit(0)

def kill_progress():
    global p
    p.kill()

def start_watch():
    event_handler = when_file_chanage(kill_progress, harakiri)
    observer = Observer(timeout=1)
    observer.schedule(event_handler, path=os.getcwd(), recursive=True)
    observer.start()
    global p, job_name, job, args
    cmd = ["uwsgi", "--json", job_name]
    if not docker_mode:
        cmd.append("--chmod-socket=666")
    if not args.debug:
        cmd.append("--logto")
        cmd.append("./logs/{}.log".format(job))
        cmd.append("--threaded-logger")
        cmd.append("--log-master")
        cmd.append("--disable-logging")
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
    return_code = p.poll()
    while return_code is None:
        sleep_time = 1
        if args.debug:
            sleep_time = 0.05
        time.sleep(sleep_time)
        if not observer.is_alive():
            kill_progress()
            break
        return_code = p.poll()
        if args.debug:
            line_byte = p.stderr.readline()
            try:
                line = line_byte.decode("ISO-8859-1")
            except UnicodeDecodeError:
                line = line_byte.decode("UTF-8")
            line = line.strip()
            if len(line) != 0:
                print(line)
                sys.stderr.flush()
            while len(line) != 0:
                line_byte = p.stderr.readline()
                try:
                    line = line_byte.decode("ISO-8859-1")
                except UnicodeDecodeError:
                    line = line_byte.decode("UTF-8")
                line = line.strip()
                print(line)
                sys.stderr.flush()
    observer.stop()
    return return_code

parser = argparse.ArgumentParser()
parser.add_argument("--main", action="store_true",
                    help=argparse.SUPPRESS)
parser.add_argument("--control", action="store_true",
                    help="If you need to monitor the control server, add this option")
parser.add_argument("--debug", action="store_true",
                    help="Debug mode")
args = parser.parse_args()
job_name = "uwsgi.json"
job = "main"
if not args.debug:
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
if args.control:
    job_name = "uwsgi.json:control"
    job = "control"
    control = True

console.log("info", "Started SilverBlog {} server".format(job))

signal.signal(signal.SIGINT, KILL_handler)
signal.signal(signal.SIGTERM, KILL_handler)
signal.signal(signal.SIGQUIT, KILL_handler)
signal.signal(signal.SIGHUP, HUP_handler)
result_code = 0
while result_code != 1:
    result_code = start_watch()
console.log("Error", "Received 1 signal,exited.")
exit(1)
