import urllib2,urllib
import json
URL= "http://127.0.0.1/clt"
post = {'item1':1,'item2':2}

data = json.dumps(post)

request = urllib2.Request(URL, data)
request.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(request)
content = response.read()
print content


