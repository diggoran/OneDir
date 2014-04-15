__author__ = 'tba5jb'

import requests
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import json

if __name__ == "__main__":
    response = requests.get("http://127.0.0.1:8000/request/")
    csrf_token = str(response.headers['set-cookie']).split('=')[1].split(';')[0]
    data = {'csrfmiddlewaretoken': csrf_token}
    headers = {}
    file_data = {'file':['test.txt', File(open('test.txt', 'rb'))]}
    response = requests.post("http://127.0.0.1:8000/request/", data=data, headers=headers, files=file_data)