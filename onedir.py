__author__ = 'kendrickjunerto'

__author__ = 'bfs8vb'

from threading import Thread
import time
import os
from Queue import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from path import LOCAL_FOLDER
from datetime import datetime

queue = Queue(10)
watching = True

def syncOneDir():
    global watching
    if watching == True:
        watching = False
    else:
        watching = True

def WatchingStatus():
    global watching
    status = watching
    return status


class ProducerThread(Thread):
    def run(self):
        global queue
        global watching
        path = os.getcwd()  + LOCAL_FOLDER
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
            if WatchingStatus() == True:
                queue.get()
                #print queue.get()
            else:
                continue

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

if __name__ == "__main__":
    ProducerThread().start()
    ConsumerThread().start()
