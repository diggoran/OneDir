__author__ = 'tba5jb'

import requests
from django.core.files import File
import json

if __name__ == "__main__":
    payload = {'key1': 'value1', 'key2': 'value2'}
    headers = {'content-type': 'application/json'}
    response = requests.post("http://127.0.0.1:8000/request/", data=json.dumps(payload), headers=headers)
    # print response.content
    # with open('/test.txt', 'r') as f:
    #     test_file = File(f)