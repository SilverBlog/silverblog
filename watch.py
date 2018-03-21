import argparse
import os
import signal
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

p = None

class when_file_chanage(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory or not os.path.basename(os.path.dirname(event.src_path)) == "static_page":
            if event.src_path.endswith('.json') or event.src_path.endswith('.md') or event.src_path.endswith(
                    'init.py') or event.src_path.endswith('.xml') or event.src_path.endswith('control_server.py'):
                p.send_signal(1)

def HUP_handler(signum, frame):
    p.send_signal(1)
def INT_handler(signum, frame):
    p.kill()
    exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("--control", action="store_true",
                    help="If you need to monitor the control server, add this option")
args = parser.parse_args()

job_name = "uwsgi.json"

if args.control:
    job_name = "uwsgi.json:control"

cmd = ["uwsgi", "--json", job_name, "--worker-reload-mercy", "1", "--reload-mercy", "4"]

p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
return_code = p.poll()

signal.signal(signal.SIGINT, INT_handler)
signal.signal(signal.SIGHUP, HUP_handler)
event_handler = when_file_chanage()
observer = Observer(timeout=10)
observer.schedule(event_handler, path=os.getcwd(), recursive=True)
observer.start()

while return_code is None:
    if not observer.is_alive():
        observer.start()
    return_code = p.poll()
    line = p.stderr.readline().strip().decode("utf-8")
    if len(line) != 0:
        print(line)
        sys.stderr.flush()
    time.sleep(0.01)

print("[{}] process has been killed.".format(job_name))
observer.stop()
exit(return_code)
