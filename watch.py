#!/usr/bin/python3

import argparse
import os
import signal
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

if os.path.exists("./install/install.lock"):
    import json

    f = open("./install/install.lock", newline=None)
    install_info = json.loads(f.read())
    if install_info["install"] == "docker":
        print("Observer performed by polling method.")
        from watchdog.observers.polling import PollingObserver as Observer
p = None
control = False

class when_file_chanage(FileSystemEventHandler):
    def __init__(self, fn):
        super().__init__()
        self.kill = fn
    def on_any_event(self, event):
        if not os.path.basename(os.path.dirname(event.src_path)) == "static_page":
            if not control and (
                    event.src_path.endswith('.json') or event.src_path.endswith('.md') or event.src_path.endswith(
                    'init.py') or event.src_path.endswith('.xml') or event.src_path.endswith('.html')):
                self.kill()
            if event.src_path.endswith('.py') and control:
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
    observer = Observer(timeout=1)
    observer.schedule(event_handler, path=os.getcwd(), recursive=True)
    observer.start()
    global p, job_name
    cmd = ["uwsgi", "--json", job_name]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
    return_code = p.poll()
    while return_code is None:
        if not observer.is_alive():
            kill_progress()
            break
        return_code = p.poll()
        line_byte = p.stderr.readline()
        try:
            line = line_byte.decode("ISO-8859-1")
        except UnicodeDecodeError:
            line = line_byte.decode("UTF-8")
        line = line.strip()
        if len(line) != 0:
            print(line)
            sys.stderr.flush()
        time.sleep(0.01)
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
print("Received 1 signal,exited.")
exit(1)
