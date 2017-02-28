import RPi.GPIO as GPIO
import httplib2
import time
import base64
import smtplib
from email.mime.text import MIMEText
import json
import sys
import os
import subprocess
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import datetime

if(len(sys.argv) < 3):
    print "Please provide argument : producer/consumer and Kafka REST server ip."
    exit(1)

# producer/consumer
type = sys.argv[1]
REST_SERVER = sys.argv[2]

# Enable producer/consumer
producer=False
consumer=False


if(type.lower() == "producer"):
    producer=True
elif(type.lower() == "consumer"):
    consumer=True
else:
    print "Only producer and consumer arguments supported"
    exit(1)


URL = "http://" + REST_SERVER + ":8082"
TOPIC = "notify"
BELL_TOPIC = "bellNotify"

# Producer variable
PRODUCE_URL = URL + "/topics/" + BELL_TOPIC

# Consumer variables
GROUP = "grp2"
CONSUMER_JSON = "consumer_json"
CONSUMER_RECORD_BINARY = "consumer_record_binary"
CONSUMER_BELL_BINARY = "consumer_bell_binary"
CONSUMER_CREATE_URL = URL + "/consumers/" + GROUP
CONSUMER_DELETE_URL = URL + "/consumers/" + GROUP + "/instances/"
CONSUMER_CONSUME_RECORD_URL = URL + "/consumers/" + GROUP + "/instances/" + CONSUMER_RECORD_BINARY + "/topics/" + TOPIC
CONSUMER_CONSUME_BELL_URL = URL + "/consumers/" + GROUP + "/instances/" + CONSUMER_BELL_BINARY + "/topics/" + BELL_TOPIC

# Send Bell notification
def send_bell_notification():
  BELL_PLAYER = 'omxplayer'
  BELL_MP3 = '/home/pi/Bell-Project/BellRingingProject/bell-ring-01.mp3'
  #BELL_PLAY = BELL_PLAYER + ' -o alsa ' + BELL_MP3 + '&'
  BELL_PLAY = BELL_PLAYER + ' -o local ' + BELL_MP3 + '&'
  subprocess.Popen([BELL_PLAYER,
                  '-o',
                  'alsa',
                  BELL_MP3])
 # os.system(BELL_PLAY);

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
        text = text + "Customer name: " + costumers[i] + "\n"
        text = text + "Deal size: " + deals[i] + "\n"

    # Above text in table format
    table_text = ""
    for i in range(0, size):
        table_text += "<tr>"
        table_text += "<td width='50%'>" + costumers[i] + "</td>"
        table_text += "<td width='50%'>" + deals[i] + "</td>"
        table_text += "</tr>"
        
    me = "maprbell2017@gmail.com"
    recipients = ['sarjeetsingh@mapr.com', 'kparadkar@mapr.com', 'mkaseebhotla@mapr.com']

    msg = MIMEMultipart('related')
    msg['Subject'] = 'Bell Project deal notification'
    msg['From'] = me
    msg['To'] = ", ".join(recipients)

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
    fp = open('/home/pi/Bell-Project/BellRingingProject/bell.png', 'rb')
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
        s.sendmail(me, recipients, msg.as_string())
    finally:
        s.quit()

def create_consumer_json():
    CONSUMER_POST_DATA = {}
    CONSUMER_POST_DATA["name"] = CONSUMER_JSON
    CONSUMER_POST_DATA["format"] = "json"
    CONSUMER_POST_DATA["auto.offset.reset"] = "earliest"
    json_data = json.dumps(CONSUMER_POST_DATA)

    headers = {}
    headers["Content-type"] = "application/vnd.kafka.v1+json"
    h = httplib2.Http()
    resp, content = h.request(CONSUMER_CREATE_URL, method="POST", body=json_data, headers=headers)
    print resp.status, content

def create_consumer_binary(consumer_name):
    CONSUMER_POST_DATA = {}
    CONSUMER_POST_DATA["name"] = consumer_name
    CONSUMER_POST_DATA["format"] = "binary"
    CONSUMER_POST_DATA["auto.offset.reset"] = "earliest"
    json_data = json.dumps(CONSUMER_POST_DATA)

    headers = {}
    headers["Content-type"] = "application/vnd.kafka.v1+json"
    h = httplib2.Http()
    resp, content = h.request(CONSUMER_CREATE_URL, method="POST", body=json_data, headers=headers)
    print resp.status, content

def delete_consumer_instances(consumer_name):
    h = httplib2.Http()
    resp, content = h.request(CONSUMER_DELETE_URL + CONSUMER_JSON, method="DELETE")
    print resp.status, content

    h = httplib2.Http()
    resp, content = h.request(CONSUMER_DELETE_URL + consumer_name, method="DELETE")
    print resp.status, content

def produce_bell_notification():
    TIMESTAMP = time.time()
    json_data='{"records":[{"key":"bell", "value":"%s"}]}' % (TIMESTAMP)
    print json_data
    
    headers = {}
    headers["Content-type"] = "application/vnd.kafka.json.v1+json"
    h = httplib2.Http()

    print PRODUCE_URL
    resp, content = h.request(PRODUCE_URL, method="POST", body=json_data, headers=headers)
    print resp.status, content

def configure_gpio():
    # Initial pin setup
    # Setup GPIO using BCM numbering
    GPIO.setmode(GPIO.BCM)
    # Set pin number 16 (GPIO23) set as input pin 
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def cleanup_gpio():
    GPIO.cleanup()

#########################################
########## Producer #####################
#########################################
if(producer):
    BELL_EVENT = False
    configure_gpio()
    while (True):
      if not BELL_EVENT:
          i = 0
          # Detect vibration while loop
          start = time.time()
          # do not consider random sparse vibrations
          # wait 15secs for consecutive 5 vibrations
          diff = 15000
          while ((i < 5) and (time.time() - start <= diff)):
              GPIO.wait_for_edge(23, GPIO.RISING)
              print i
              i = i + 1
              GPIO.wait_for_edge(23, GPIO.FALLING)
              
          if i >= 5:
              # bell notification occured 
              legit_event = 'Legit event, Ring the Bell!'
              print legit_event
              BELL_EVENT = True
              produce_bell_notification()
        
          if BELL_EVENT:
              BELL_EVENT = False
       
      time.sleep(2)

#########################################
########## Consumer #####################
#########################################
DECOUPLE_EVENTS = False
WAIT_TIME_MS = 10 * 60 * 1000 # 10 Min
if(consumer):

    # Delete consumer instances (json/binary) if exists already
    #delete_consumer_instances(CONSUMER_BELL_BINARY)
    #delete_consumer_instances(CONSUMER_RECORD_BINARY)

    # Create new instance of consumer
    create_consumer_binary(CONSUMER_BELL_BINARY)
    create_consumer_binary(CONSUMER_RECORD_BINARY)

    # Start consumer
    print CONSUMER_CONSUME_RECORD_URL
    headers1 = {}
    headers1["Accept"] = "application/vnd.kafka.binary.v1+json"
    h = httplib2.Http()
    while (True):
        resp_bell, content_bell = h.request(CONSUMER_CONSUME_BELL_URL, method="GET", headers=headers1)
        if len(content_bell) > 2:
            print resp_bell, content_bell
            # Bell notification present
            resp_record, content_record = h.request(CONSUMER_CONSUME_RECORD_URL, method="GET", headers=headers1)
            print resp_record, content_record
            if DECOUPLE_EVENTS:
                send_bell_notification()
                if len(content_record) > 2:  # length=2 is []
                    send_email(content_record)
            else:
                if len(content_record) > 2: 
                    # Record present
                    send_bell_notification()
                    send_email(content_record)
                else:
                    # Record absent
                    wait_start = time.time()
                    # Wait for 10 mins for record to appear or discard notification
                    while (time.time() - wait_start < WAIT_TIME_MS):
                         resp_record, content_record = h.request(CONSUMER_CONSUME_RECORD_URL, method="GET", headers=headers1)
                         if len(content_record) > 2:
                              # Record occured within WAIT_TIME_MS
                              send_bell_notification()
                              send_email(content_record) 
                              break
                         else:
                              time.sleep(2)
        else:
            print "\nWaiting for Bell notification."

        time.sleep(2)  # Wait 2 sec before consuming
