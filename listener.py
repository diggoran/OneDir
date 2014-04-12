__author__ = 'bfs8vb'

import sys
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if (event.is_directory):
            print ("Directory modified on %s" % time.ctime())
            print ("\t%s" % event.src_path)
        else:
            print ("File modified on %s" % time.ctime())
            print ("\t%s" % event.src_path)

    def on_created(self, event):
        if (event.is_directory):
            print ("Directory created on %s" % time.ctime())
            print ("\t%s" % event.src_path)
        else:
            print ("File created on %s" % time.ctime())
            print ("\t%s" % event.src_path)

    def on_moved(self, event):
        if (event.is_directory):
            print ("Directory moved on %s" % time.ctime())
            print ("\tFrom:\t %s" % event.src_path)
            print ("\tTo:\t\t %s" % event.dest_path)
        else:
            print ("File moved on %s" % time.ctime())
            print ("\tFrom:\t %s" % event.src_path)
            print ("\tTo:\t\t %s" % event.dest_path)

    def on_deleted(self, event):
        if (event.is_directory):
            print ("Directory deleted on %s" % time.ctime())
            print ("\t%s" % event.src_path)
        else:
            print ("File deleted on %s" % time.ctime())
            print ("\t%s" % event.src_path)

if __name__ == "__main__":

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