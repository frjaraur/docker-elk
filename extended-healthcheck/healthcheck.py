#!/usr/bin/python3
import os
import json
from pprint import pprint
import socket
import time
import requests

OUTFILE='/tmp/output.json'



def Debug(text):
    if DEBUG == "True": print ("DEBUG: "+text)


def Minor(text):
    print ("ERROR: "+text)

def Critical(text):
    print ("ERR: "+text)
    print ("Can not continue....")
    exit()

def GetUrlData(url):
	r = requests.get(url)
	status=r.status_code
	headers=r.headers['content-type']
	encoding=r.encoding
	text=r.text
	jsondata=r.json()

#########
#
# LOGSTASH_HOST
try:
     LOGSTASH_HOST=os.environ['LOGSTASH_HOST']
except KeyError:
    Critical("Logstash host is required")

try:
     LOGSTASH_PORT=os.environ['LOGSTASH_PORT']
except KeyError:
     LOGSTASH_PORT=5000

try:
     SERVICE=os.environ['SERVICE']
except KeyError:
     SERVICE="testservice"

try:
     APPLICATION=os.environ['APPLICATION']
except KeyError:
     APPLICATION="testapp"

try:
     DEBUG=os.environ['DEBUG']
except KeyError:
     DEBUG="False"



def FeedLogstash(hostname, port, content):
	Debug("Connection to "+hostname+" on port "+port)
	try:
            port=int(port)
	except:
            Critical("Port is not a number... integer required")

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	jcontent=json.dumps(content, ensure_ascii=False)
	try:
            pprint(content)
            #s.setblocking(True)
            s.connect((hostname, port))
            #s.send(content.encode())
            #msg = {'@message': 'python test message', '@tags': ['python', 'test']}
            #jmsg=json.dumps(msg)
            #s.send(jmsg.encode())
            jcontent=json.dumps(content)
            s.send(jcontent.encode())
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            Debug ("FeedLogstash: Sent Data")
            pprint(content)
	except Exception as err:
                Minor ("Can not connect... ("+str(err)+")")









with open(OUTFILE) as data_file:
    metrics = json.load(data_file)

#pprint(data)

metrics['SERVICE']=SERVICE
metrics['APPLICATION']=APPLICATION
metrics['@type']=APPLICATION
iso_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
metrics['@timestamp']=iso_time

for key,value in metrics.items():
    print (key+"-->"+str(value))

#pprint(metrics)

FeedLogstash(LOGSTASH_HOST,LOGSTASH_PORT,metrics)
