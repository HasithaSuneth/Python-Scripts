# python script_name.py &
# Start-Process python -ArgumentList ".\FileTimeStampSync.py" -NoNewWindow


import os
import time
import shutil
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileSyncHandler(FileSystemEventHandler):
    def __init__(self, src_file, target_path, target_name):
        self.src_file = src_file
        self.target_path = target_path
        self.target_name = target_name

    def on_modified(self, event):
        if event.src_path == self.src_file:
            print("File modified, syncing...")
            target_file = os.path.join(self.target_path, self.target_name)
            shutil.copy2(self.src_file, target_file)
            print("Sync complete")

def stop_sync(signal, frame):
    global observer
    observer.stop()
    observer.join()

def main():
    src_file = "source-file"
    target_path = "target-path"
    target_name = "target-file"

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    shutil.copy2(src_file, os.path.join(target_path, target_name))
    print("Initial synchronization complete")

    global observer
    event_handler = FileSyncHandler(src_file, target_path, target_name)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(src_file), recursive=False)
    observer.start()

    signal.signal(signal.SIGINT, stop_sync)
    signal.signal(signal.SIGTERM, stop_sync)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_sync(None, None)

if __name__ == "__main__":
    main()
