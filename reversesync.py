import calendar
import requests
from datetime import datetime, timedelta
import json
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
	    print 'http://127.0.0.1:8000/download/admin'+path
	    response = requests.get('http://127.0.0.1:8000/download/admin/'+path, stream=True)
	    if not response.ok:
	        # Something went wrong
	        print "something went wrong"
	    for block in response.iter_content(1024):
	        if not block:
	            break
	        handle.write(block)	
