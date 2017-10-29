import argparse
import os
import signal
import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class when_file_chanage(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.src_path.endswith((".", ".swp", ".sh")):
            p.send_signal(1)


def HUP_handler(signum, frame):
    p.send_signal(1)
def INT_handler(signum, frame):
    p.kill()
    exit(0)



if __name__ == "__main__":
    cmd = ["uwsgi", "--json", "uwsgi.json"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--docker",
                        help="When running in the docker, please add this command to speed up the restart of the program",
                        action="store_true")
    args = parser.parse_args()
    if args.docker:
        cmd.extend(["--worker-reload-mercy", "1", "--reload-mercy", "4"])
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
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
            time.sleep(0.05)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    exit(return_code)
