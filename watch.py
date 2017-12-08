import argparse
import os
import signal
import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

control_p = None
p = None


class when_file_chanage(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.src_path.endswith((".", ".swp", ".sh")):
            p.send_signal(1)

def HUP_handler(signum, frame):
    p.send_signal(1)
    if control_p is not None:
        control_p.send_signal(1)

def INT_handler(signum, frame):
    p.kill()
    if control_p is not None:
        control_p.kill()
    exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker",
                        help="When running in the docker, please add this command to speed up the restart of the program",
                        action="store_true")
    parser.add_argument("--control", action="store_true",
                        help="If you need to monitor the control server, add this option")
    args = parser.parse_args()

    if args.control:
        control_cmd = ["uwsgi", "--json", "uwsgi.json:control"]
        control_p = subprocess.Popen(control_cmd, stderr=subprocess.PIPE)

    cmd = ["uwsgi", "--json", "uwsgi.json"]
    if args.docker:
        cmd.extend(["--worker-reload-mercy", "1", "--reload-mercy", "4"])
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE)
    return_code = p.poll()
    signal.signal(signal.SIGINT, INT_handler)
    signal.signal(signal.SIGHUP, HUP_handler)
    event_handler = when_file_chanage()
    observer = Observer()
    observer.schedule(event_handler, path=os.getcwd(), recursive=True)
    observer.start()
    try:
        while return_code is None:
            line = p.stderr.readline()
            return_code = p.poll()
            line = line.strip().decode("utf-8")
            if len(line) != 0:
                print(line)
            time.sleep(0.01)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    exit(return_code)
