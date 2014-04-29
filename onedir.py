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
import json

queue = Queue(10)
syncing = True
adding = False


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
            print task['command'] + ": " + task['src_path']
            if "goutputstream" not in task['src_path']:
                if task['command'] == 'file_created':
                    print "Adding File!"
                    with File(open(task['src_path'], 'rb')) as upload:
                        data = {'path': os.path.split(task['src_path'])[0].split(LOCAL_FOLDER, 1)[1].strip('\\').strip('/'), 'file_name': os.path.split(task['src_path'])[1], 'username':'admin', 'password':'password', 'size':7}
                        files = {'file': [os.path.split(task['src_path'])[1], upload]}
                        print data
                        requests.post("http://127.0.0.1:8000/upload/", data=data, files=files)
                        #doesn't like spaces in file name
                        #can't save to main directory
                        #putting entire path+filename in the file info makes saving to main but not other folders possible
                        #working on a fix on Monday
                    adding=True

                elif task['command'] == 'file_modified':
                    if not adding: 
                        print "Modifying File!"
                        data = {'user_name': 'admin', 'path': task['src_path'].rsplit('/', 1)[0].split(LOCAL_FOLDER, 1)[1].strip('/').strip('/'), 'file_name': task['src_path'].rsplit('/', 1)[1], 'password':'password'}
                        requests.post("http://127.0.0.1:8000/delete/", data=data)
                        with File(open(task['src_path'], 'rb')) as upload:
                            data = {'path': os.path.split(task['src_path'])[0].split(LOCAL_FOLDER, 1)[1].strip('\\').strip('/'), 'file_name': os.path.split(task['src_path'])[1], 'user_name':'admin', 'password':'password', 'size':7}
                            print data
                            files = {'file': [os.path.split(task['src_path'])[1], upload]}
                            requests.post("http://127.0.0.1:8000/upload/", data=data, files=files)
                    else: 
                        print "--modify called but its due to a create--"
                        adding=False
                elif task['command'] == 'file_deleted':
                    print "deleting file"
                    # print task['src_path']
                    # print task['src_path'].rsplit('/', 1)[0].split(LOCAL_FOLDER, 1)[1].strip('/').strip('/')
                    # print task['src_path'].rsplit('/', 1)[1]
                    data = {'user_name': 'admin', 'path': task['src_path'].rsplit('/', 1)[0].split(LOCAL_FOLDER, 1)[1].strip('/').strip('/'), 'file_name': task['src_path'].rsplit('/', 1)[1], 'password':'password'}
                    requests.post("http://127.0.0.1:8000/delete/", data=data)
                else:    
                    print "--" + task['command'] + "--"
            # if task['command'] == 'blah':
            #     data = {'user_id': 'tba5jb', 'path': task['src_path'].rsplit('\\', 1)[0].split(LOCAL_FOLDER, 1)[1].strip('\\')}
            #     requests.post("http://127.0.0.1:8000/upload/", data=data)


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
        print event


def toggle_sync():
    global syncing
    syncing = not syncing

def update_files(username):
    today = datetime.now()
    dt=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print dt
    data = {'timestamp': dt}
    response = requests.post("http://127.0.0.1:8000/latestchanges/", data=data)
    print response.text
    result=json.loads(response.text)
    for r in result['files']:
        file_name = r.split('/')[-1]
        path = r
        with open('watched/'+path, 'wb') as handle:
            #print 'http://127.0.0.1:8000/download/'+username+'/'+path
            response = requests.get('http://127.0.0.1:8000/download/'+username+'/'+ path, stream=True)
            if not response.ok:
                # Something went wrong
                print "something went wrong"
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block) 

def is_syncing():
    global syncing
    return syncing

if __name__ == "__main__":
    ProducerThread().start()
    ConsumerThread().start()
