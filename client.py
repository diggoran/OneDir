__author__ = 'kendrickjunerto'

__author__ = 'bfs8vb'

import os
from OneDir import ProducerThread, ConsumerThread, syncOneDir, WatchingStatus,queue
import sys
from threading import Thread
import shutil
from path import LOCAL_FOLDER, BASE_ADDRESS
import requests
from datetime import datetime

"""class LocalClient():
    def __init__(self,name, password, watched, syncStatus):
        self.username = name
        self.password = password
        self.watched = watched
        self.sync = syncStatus"""

def makeDir():
    if not os.path.exists(os.getcwd() + LOCAL_FOLDER):
        os.mkdir(os.getcwd() + LOCAL_FOLDER)
    else:
        print LOCAL_FOLDER + " already exists."

def register(NewUsername, NewPassword):
    userdata = {'username' : NewUsername, 'password': NewPassword}
    response = requests.post(BASE_ADDRESS+ "loginrequest/", data=userdata)
    return response
    #return True

def login(Username, Password):
    loginUserdata = {'username' : Username, 'password': Password}
    response = requests.post(BASE_ADDRESS+ "loginrequest/", data=loginUserdata)
    return response
    #return True

logged_in = False

if sys.argv[1] == "start":
    while True:
        print "Choose the following options: "
        print "1. Login to your OneDir account now."
        print "2. Register for a new OneDir account."
        print "3. Turn off On or Off my OneDir Sync"
        print "4. Log out of My OneDir Account."
        UserInput = raw_input()
        if UserInput == "1":
            print "Please enter your username: "
            Username = raw_input()
            print "Please enter your password: "
            Password = raw_input()
            permission = login(Username, Password)
            if permission:
                makeDir()
                print "You are now logged in to OneDir and can begin using OneDir. "
                logged_in = True
                ProducerThread().start()
                ConsumerThread().start()
                print WatchingStatus()

        if UserInput == "2":
            print "Please enter a new username: "
            NewUsername = raw_input()
            print "Please enter a password: "
            NewPassword = raw_input()
            print "Please enter password again: "
            RepeatPassword = raw_input()
            while NewPassword != RepeatPassword:
                print "your passwords don't match."
                print "Please enter a password: "
                NewPassword = raw_input()
                print "Please enter password again: "
                RepeatPassword = raw_input()
            permission = register(NewUsername, NewPassword)
            if permission:
                makeDir()
                print "Congrats! You are now registered as a OneDir user and automatically logged in. Begin Using OneDir."
                logged_in = True
                ProducerThread().start()
                ConsumerThread().start()


        if UserInput == "3":
            watching = WatchingStatus()
            if logged_in == True:
                if watching:
                    print "Sync is being turned off. All modifications will not be recorded from now on."
                    syncOneDir()
                    sync_Command = {'command': 'syncoff' , 'src_path': '','dest_path': '', 'time': datetime.now()}
                    sync_Command2 =  {'command': 'syncoff' , 'src_path': '','dest_path': '', 'time': datetime.now()}
                    queue.put(sync_Command)
                    queue.put(sync_Command2)
                    print WatchingStatus()

                else:
                    print "Now turning on sync. All modifications will be recorded from now on."
                    syncOneDir()
                    print WatchingStatus()
            else:
                print "Please login to OneDir or register for a new account with OneDir."

        if UserInput == "4":
            if logged_in == True:
                logged_in = False
                print "Logging out of OneDir."
                print "You can now log in with another account or register a new account."
            else:
                print "You cannot log out when you are not logged in."



"""if __name__ == "__main__":

#client = LocalClient()"""