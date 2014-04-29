__author__ = 'tba5jb'

import requests
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import json

if __name__ == "__main__":
    # response = requests.get("http://127.0.0.1:8000/request/")
    # csrf_token = str(response.headers['set-cookie']).split('=')[1].split(';')[0]
    # data = {'csrfmiddlewaretoken': csrf_token}
    # data = {}
    # headers = {}
    # command = queue.get()
    # if(command.task == 'newFile'):
    #     files = {'file':[command.file, File(open('test.txt', 'rb'))]}
    #     response = requests.post("http://127.0.0.1:8000/request/", files=files)
    data = {'username': 'admin', 'password':'password', 'size': 7, 'path': 'derp/file.txt', 'file_name':'file.txt'}
    files = {'file': ['test.txt', File(open('watched/derp/file.txt', 'rb'))]}
    response = requests.post("http://127.0.0.1:8000/upload/", data=data, files=files)
    print response.text
    # response = requests.post("http://127.0.0.1:8000/request/", data=data, headers=headers, files=files)