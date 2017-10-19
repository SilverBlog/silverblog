import argparse
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
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
return_code = p.poll()


class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.src_path != ".":
            p.send_signal(1)


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while return_code is None:
            line = p.stderr.readline()
            return_code = p.poll()
            line = line.strip().decode("utf-8")
            if len(line) != 0:
                print(line)
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    exit(return_code)
