__author__ = 'kendrickjunerto'

__author__ = 'bfs8vb'

from threading import Thread
import time
import os
from Queue import Queue
from django.core.files import File
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from path import LOCAL_FOLDER
from datetime import datetime
import requests

queue = Queue(10)
syncing = True


class ProducerThread(Thread):
    def run(self):
        global queue
        global syncing
        path = os.path.join(os.getcwd(), LOCAL_FOLDER)
        while True:
            event_handler = Handler()
            observer = Observer()
            observer.schedule(event_handler, path, recursive=True)
            observer.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()


class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            task = queue.get()
            if task['command'] == 'file_created':
                with File(open(task['src_path'], 'rb')) as upload:
                    print "create file!"
                    data = {'user_id': 'tba5jb', 'path': task['src_path'].rsplit('\\', 1)[0].split(LOCAL_FOLDER, 1)[1].strip('\\')}
                    files = {'file': [task['src_path'].rsplit('\\', 1)[1], upload]}
                    requests.post("http://127.0.0.1:8000/upload/", data=data, files=files)


class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            queue.put({'command': "dir_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': datetime.now()})
        else:
            queue.put({'command': "file_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': datetime.now()})

    def on_created(self, event):
        if event.is_directory:
            queue.put({'command': "dir_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': datetime.now()})
        else:
            queue.put({'command': "file_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': datetime.now()})

    def on_moved(self, event):
        if event.is_directory:
            queue.put({'command': "dir_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': event.dest_path, 'time': datetime.now()})
        else:
            queue.put({'command': "file_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': event.dest_path, 'time': datetime.now()})

    def on_deleted(self, event):
        if event.is_directory:
            queue.put({'command': "dir_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': datetime.now()})
        else:
            queue.put({'command': "file_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': datetime.now()})


def toggle_sync():
    global syncing
    syncing = not syncing


def is_syncing():
    global syncing
    return syncing


if __name__ == "__main__":
    ProducerThread().start()
    ConsumerThread().start()
