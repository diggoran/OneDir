__author__ = 'bfs8vb'

import os

class LocalClient():
    def __init__(self):
        self.username = "name"
        self.password = "pass"
        self.watched = os.getcwd() + "\watched"
        self.sync = False

    def changePass(self):
        print ("Type current password.")
        check = raw_input()
        if check == self.password:
            print ("Type new password.")
            newPass = raw_input()
            self.password = newPass
            print ("Password successfully changed.")
        else:
            print("Incorrect password.")

    def changeName(self):
        print ("Type current password.")
        check = raw_input()
        if check == self.password:
            print ("Type new username.")
            newName = raw_input()
            self.username = newName
            print ("Username successfully changed.")
        else:
            print("Incorrect password.")

if __name__ == "__main__":

    client = LocalClient()