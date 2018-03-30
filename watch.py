#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
import signal
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

p = None
control = False

class when_file_chanage(FileSystemEventHandler):
    def __init__(self, fn):
        super().__init__()
        self.kill = fn
    def on_any_event(self, event):
        if not os.path.basename(os.path.dirname(event.src_path)) == "static_page":
            if not control:
                if event.src_path.endswith('.json') or event.src_path.endswith('.md') or event.src_path.endswith(
                        'init.py') or event.src_path.endswith('.xml'):
                    self.kill()
            if event.src_path.endswith('control_server.py') and control:
                self.kill()

def HUP_handler(signum, frame):
    kill_progress()

def KILL_handler(signum, frame):
    global p
    os.killpg(os.getpgid(p.pid), signal.SIGINT)
    exit(0)

def kill_progress():
    global p
    p.kill()

def start_watch():
    event_handler = when_file_chanage(kill_progress)
    observer = Observer(timeout=0.01)
    observer.schedule(event_handler, path=os.getcwd(), recursive=True)
    observer.start()
    global p, job_name
    cmd = ["uwsgi", "--json", job_name]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
    return_code = p.poll()
    while return_code is None:
        return_code = p.poll()
        line = p.stderr.readline().strip().decode("utf-8")
        if len(line) != 0:
            print(line)
            sys.stderr.flush()
        time.sleep(0.01)
    observer.stop()
    return return_code

parser = argparse.ArgumentParser()
parser.add_argument("--control", action="store_true",
                    help="If you need to monitor the control server, add this option")
args = parser.parse_args()
job_name = "uwsgi.json"
job = "main"
if args.control:
    job_name = "uwsgi.json:control"
    job = "control"
    control = True
for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]:
    signal.signal(signal.SIGINT, KILL_handler)
signal.signal(signal.SIGHUP, HUP_handler)
result_code = 0
while result_code != 1:
    result_code = start_watch()
exit(result_code)
