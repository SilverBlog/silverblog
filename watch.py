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

kill_send = False
p = None
control = False

class when_file_chanage(FileSystemEventHandler):
    def on_any_event(self, event):
        if not os.path.basename(os.path.dirname(event.src_path)) == "static_page":
            if not control:
                if event.src_path.endswith('.json') or event.src_path.endswith('.md') or event.src_path.endswith(
                        'init.py') or event.src_path.endswith('.xml'):
                    p.send_signal(1)
            if event.src_path.endswith('control_server.py') and control:
                p.send_signal(1)

def HUP_handler(signum, frame):
    p.send_signal(signum)

def KILL_handler(signum, frame):
    global kill_send
    if not kill_send:
        kill_send = True
        print("[{}] process has been killed.".format(job))
    #p.kill()
    os.killpg(os.getpgid(p.pid), signum)
    exit(0)

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
cmd = ["uwsgi", "--json", job_name, "--worker-reload-mercy", "1", "--reload-mercy", "4"]

p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
return_code = p.poll()

for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]:
    signal.signal(signal.SIGINT, KILL_handler)

signal.signal(signal.SIGHUP, HUP_handler)

event_handler = when_file_chanage()
observer = Observer()
observer.schedule(event_handler, path=os.getcwd(), recursive=True)
observer.start()

while return_code is None:
    if not observer.is_alive():
        print("Watch process has been killed.".format(job))
        exit(1)
    return_code = p.poll()
    line = p.stderr.readline().strip().decode("utf-8")
    if len(line) != 0:
        print(line)
        sys.stderr.flush()
    time.sleep(0.01)
while len(line) != 0:
    line = p.stderr.readline().strip().decode("utf-8")
    print(line)
    sys.stderr.flush()
print("[{}] process has been killed.".format(job))
observer.stop()
exit(0)
