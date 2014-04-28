__author__ = 'kendrickjunerto'

__author__ = 'bfs8vb'

import os
from onedir import ProducerThread, ConsumerThread, toggle_sync, is_syncing, queue
import sys
from threading import Thread
import shutil
from path import LOCAL_FOLDER, BASE_ADDRESS
import requests
from datetime import datetime

# class LocalClient():
#     def __init__(self,name, password, watched, syncStatus):
#         self.username = name
#         self.password = password
#         self.watched = watched
#         self.sync = syncStatus


def make_dir():
    if not os.path.exists(os.getcwd() + LOCAL_FOLDER):
        os.umask(0)
        os.mkdir(os.getcwd() + LOCAL_FOLDER, 0777)
    else:
        print LOCAL_FOLDER + " already exists."


def register(username, password):
    data = {'username': username, 'password': password}
    response = requests.post(BASE_ADDRESS + "loginrequest/", data=data)
    if "success" in response:
        return True
    return False


def login(username, password):
    data = {'username': username, 'password': password}
    print data
    response = requests.post(BASE_ADDRESS + "loginrequest/", data=data)
    if "success" in response:
        return True
    return False

def logout():
    response = requests.post(BASE_ADDRESS + "logoutrequest/", data=data)
    if "success" in response:
        return True
    return False

logged_in = False

if True:#sys.argv[1] == "start":
    while True:
        print "Choose the following options: "
        print "1. Login to your OneDir account now."
        print "2. Register for a new OneDir account."
        print "3. Turn off On or Off my OneDir Sync"
        print "4. Log out of My OneDir Account."
        input = raw_input()
        if input == "1":
            print "Please enter your username: "
            username = raw_input()
            print "Please enter your password: "
            password = raw_input()
            if login(username, password):
                make_dir()
                print "You are now logged in to OneDir and can begin using OneDir. "
                logged_in = True
                ProducerThread().start()
                ConsumerThread().start()
                print "Syncing: " + str(is_syncing())
        if input == "2":
            # print "Please enter a new username: "
            # username = raw_input()
            # print "Please enter a password: "
            # password = raw_input()
            # print "Please enter password again: "
            # while password != raw_input():
            #     print "Your passwords don't match."
            #     print "Please enter a password: "
            #     password = raw_input()
            #     print "Please enter password again: "
            # if register(username, password):
            #     make_dir()
            #     print "Congrats! You are now registered as a OneDir user and automatically logged in. Begin Using OneDir."
                # logged_in = True
                # ProducerThread().start()
                # ConsumerThread().start()
            print "Please register at the following link: " + BASE_ADDRESS + "register/"
        if input == "3":
            syncing = is_syncing()
            if True:#logged_in:
                if syncing:
                    print "Sync is being turned off. All modifications will not be recorded from now on."
                    toggle_sync()
                    sync_Command = {'command': 'syncoff', 'src_path': '', 'dest_path': '', 'time': datetime.now()}
                    sync_Command2 = {'command': 'syncoff', 'src_path': '', 'dest_path': '', 'time': datetime.now()}
                    queue.put(sync_Command)
                    queue.put(sync_Command2)
                    print is_syncing()

                else:
                    print "Now turning on sync. All modifications will be recorded from now on."
                    toggle_sync()
                    print is_syncing()
            else:
                print "Please login to OneDir or register for a new account with OneDir."

        if input == "4":
            if logged_in:
                logout()
                logged_in = False
                print "Logging out of OneDir."
                print "You can now log in with another account or register a new account."
            else:
                print "You cannot log out when you are not logged in."


# if __name__ == "__main__":

#client = LocalClient()