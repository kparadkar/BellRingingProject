import httplib2
import socket
import time
import smtplib
import base64
from email.mime.text import MIMEText
import os
import json
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import datetime

URL = "http://54.219.187.57:8082"
LOCALHOST = "127.0.0.1"
TOPIC = "notify"

# method to get greet message
def get_greeting_msg():

    currentTime = datetime.datetime.now()
    print "Current hour: ", currentTime.hour

    if currentTime.hour < 12:
        return 'Good Morning,'
    elif 12 <= currentTime.hour < 18:
        return 'Good Afternoon,'
    else:
        return 'Good Evening,'

# Email method for sending email
def send_email(body):

    print "Configure email with body:" + body

    body_json=json.loads(body)
    costumers = []
    deals = []
    size = 0
    for item in body_json:
        customer = base64.b64decode((item["key"]))
        if customer.startswith('"') and customer.endswith('"'):
            customer = customer[1:-1]
        costumers.append(customer)

        deal = base64.b64decode((item["value"]))
        if deal.startswith('"') and deal.endswith('"'):
            deal = deal[1:-1]
        deals.append(deal)
        size += 1
    
    text = ""
    for i in range(0, size):
        text = text + "Customer name: " + costumers[i] + "<\n>"
        text = text + "Deal size: " + deals[i] + "<\n>"

    # Above text in table format
    table_text = ""
    for i in range(0, size):
        table_text += "<tr>"
        table_text += "<td width='50%'>" + costumers[i] + "</td>"
        table_text += "<td width='50%'>" + deals[i] + "</td>"
        table_text += "</tr>"

    me = "maprbell2017@gmail.com"
    you = "sarjeetsingh@maprtech.com"

    msg = MIMEMultipart('related')
    msg['Subject'] = 'Bell Project deal notification'
    msg['From'] = me
    msg['To'] = you

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    msgText = MIMEText(text)
    msgAlternative.attach(msgText)


    ##### Image text
    greetMsg = get_greeting_msg()
    image_txt = \
    '''
    <b>''' + greetMsg + ''' </b><br><br><img src="cid:image1"><br><br><br>
    <b> Here is the latest customer deal: </b><br><br>
    <table border="1" style="width:80%">
    <tr>
    <th>Customer name</th>
    <th>Deal Size</th>
    </tr>
    <p> ''' + table_text  + ''' </p>
    </table><br>
    <p> Thanks, <br>Bell-project team!<br>
    '''

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(image_txt, 'html')
    msgAlternative.attach(msgText)

    # Assume the image is in the current directory
    fp = open('bell.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', 'image1')
    msg.attach(msgImage)

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
        s.sendmail(me, [you], msg.as_string())
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
h = httplib2.Http()
resp, content = h.request(CONSUMER_DELETE_URL, method="DELETE")
print resp.status, content

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
