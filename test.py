import httplib2
import socket
import time
import smtplib
import base64
from email.mime.text import MIMEText
import os
import json

URL = "http://10.10.104.46:8082"
LOCALHOST = "127.0.0.1"
TOPIC = "notify"

# Email method for sending email
def send_email(body):

    print "Configure email with body:" + body

    body_json=json.loads(body)
    costumers = []
    deals = []
    size = 0
    for item in body_json:
        costumers.append (base64.b64decode((item["key"])))
        deals.append (base64.b64decode((item["value"])))
        size += 1
    
    text = ""
    for i in range(0, size):
        text = text + "Customer name: " + costumers[i] + "\n"
        text = text + "Deal size: " + deals[i] + "\n"

    print text

    text_msg = MIMEText(text, 'plain')

    me = "maprbell2017@gmail.com"
    you = "sarjeetsingh@maprtech.com"

    text_msg['Subject'] = 'Bell Project deal notification'
    text_msg['From'] = me
    text_msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    HOST = "smtp.gmail.com"
    PORT = "587"
    s = smtplib.SMTP()
    s.connect(HOST, PORT)
    USER = "maprbell2017@gmail.com"
    PASSWD = "maprmapr"
    s.starttls()
    s.login(USER, PASSWD)
    #s.set_debuglevel(True)
    try:
        s.sendmail(me, [you], text_msg.as_string())
    finally:
        s.quit()

#Producer

#########################################
######### Consumer ######################
#########################################

# Consumer variables
GROUP = "grp2"
CONSUMER = "consumer2"
CONSUMER_CREATE_URL = URL + "/consumers/" + GROUP
CONSUMER_DELETE_URL = URL + "/consumers/" + GROUP + "/instances/" + CONSUMER
CONSUMER_CONSUME_URL = URL + "/consumers/" + GROUP + "/instances/" + CONSUMER + "/topics/" + TOPIC

# Delete consumer instance if exists already
#h = httplib2.Http()
#resp, content = h.request(CONSUMER_DELETE_URL, method="DELETE")
#print resp.status, content

# Create new instance of consumer
CONSUMER_POST_DATA = {}
CONSUMER_POST_DATA["name"] = CONSUMER
CONSUMER_POST_DATA["format"] = "binary"
CONSUMER_POST_DATA["auto.offset.reset"] = "earliest"
json_data = json.dumps(CONSUMER_POST_DATA)

headers = {}
headers["Content-type"] = "application/vnd.kafka.v1+json"
h = httplib2.Http()
resp, content = h.request(CONSUMER_CREATE_URL, method="POST", body=json_data, headers=headers)
print resp.status, content

# Start consumer
print CONSUMER_CONSUME_URL
headers1 = {}
headers1["Accept"] = "application/vnd.kafka.binary.v1+json"
h = httplib2.Http()
while(True):
    resp, content = h.request(CONSUMER_CONSUME_URL, method="GET", headers=headers1)
    print resp, content
    if len(content) > 2:    # length=2 is []
        #body = content[1:len(content)-1]
        send_email(content)
    time.sleep(2) # Wait 2 sec before consuming
