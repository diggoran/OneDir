__author__ = 'bfs8vb'

from threading import Thread
import time
import os
import random
from Queue import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

queue = Queue(10)

class ProducerThread(Thread):
    def run(self):
        global queue
        path = os.getcwd() + "\watched"
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
            print queue.get()

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            queue.put({'command': "dir_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': time.ctime()})
        else:
            queue.put({'command': "file_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': time.ctime()})

    def on_created(self, event):
        if event.is_directory:
            queue.put({'command': "dir_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': time.ctime()})
        else:
            queue.put({'command': "file_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': time.ctime()})

    def on_moved(self, event):
        if event.is_directory:
            queue.put({'command': "dir_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': event.dest_path, 'time': time.ctime()})
        else:
            queue.put({'command': "file_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': event.dest_path, 'time': time.ctime()})

    def on_deleted(self, event):
        if event.is_directory:
            queue.put({'command': "dir_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': time.ctime()})
        else:
            queue.put({'command': "file_" + event.event_type, 'src_path': event.src_path,
                       'dest_path': '', 'time': time.ctime()})

if __name__ == "__main__":
    ProducerThread().start()
    ConsumerThread().start()
