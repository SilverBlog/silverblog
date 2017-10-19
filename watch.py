import argparse
import os
import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

cmd = ["uwsgi", "--json", "uwsgi.json"]

parser = argparse.ArgumentParser()
parser.add_argument("--docker", action="store_true")
args = parser.parse_args()
if args.docker:
    cmd.append("--worker-reload-mercy")
    cmd.append("1")
    cmd.append("--reload-mercy")
    cmd.append("4")
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
return_code = p.poll()


class when_file_chanage(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.src_path.endswith((".", ".swp", ".sh")):
            p.send_signal(1)  #SIGHUP


if __name__ == "__main__":
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
            time.sleep(0.05)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    exit(return_code)
