import argparse
import os
import signal
import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

control_return_code = None
docker_control_p = None
p = None
control = False

class when_file_chanage(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory or os.path.basename(os.path.dirname(event.src_path)) != "static_page":
            if event.src_path.endswith('.json') or event.src_path.endswith('.md') or event.src_path.endswith(
                    'init.py') or event.src_path.endswith('.xml'):
                if not control:
                    p.send_signal(1)
            if event.src_path.endswith('control_server.py'):
                if control:
                    p.send_signal(1)
                if docker_control_p is not None:
                    docker_control_p.send_signal(1)

def HUP_handler(signum, frame):
    p.send_signal(1)
    if docker_control_p is not None:
        docker_control_p.send_signal(1)

def INT_handler(signum, frame):
    p.kill()
    if docker_control_p is not None:
        docker_control_p.kill()
    exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("--docker",
                    help="When running in the docker, please add this command to speed up the restart of the program",
                    action="store_true")
parser.add_argument("--control", action="store_true",
                    help="If you need to monitor the control server, add this option")
args = parser.parse_args()

cmd = ["uwsgi", "--json", "uwsgi.json", "--worker-reload-mercy", "1", "--reload-mercy", "8"]

if args.control and not args.docker:
    control = True
    cmd = ["uwsgi", "--json", "uwsgi.json:control", "--worker-reload-mercy", "1", "--reload-mercy", "8"]

if args.control and args.docker:
    control_cmd = ["uwsgi", "--json", "uwsgi.json:control", "--worker-reload-mercy", "1", "--reload-mercy", "8"]
    docker_control_p = subprocess.Popen(control_cmd, stderr=subprocess.PIPE)
    control_return_code = docker_control_p.poll()

p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
return_code = p.poll()

control_line = ""
signal.signal(signal.SIGINT, INT_handler)
signal.signal(signal.SIGHUP, HUP_handler)
event_handler = when_file_chanage()
observer = Observer(timeout=10)
observer.schedule(event_handler, path=os.getcwd(), recursive=True)
observer.start()
while return_code is None:
    return_code = p.poll()
    if args.control and args.docker:
        if control_return_code is not None:
            break
        control_return_code = docker_control_p.poll()
        control_line = docker_control_p.stderr.readline().strip().decode("utf-8")
        if len(control_line) != 0:
            print("[control] " + control_line)
    line = p.stderr.readline().strip().decode("utf-8")
    if len(line) != 0:
        head = "[main] "
        if control:
            head = "[control] "
        print(head + line)
    time.sleep(0.01)

if return_code is not None:
    exit(return_code)
exit(control_return_code)
