# This Python file uses the following encoding: utf-8

# -----Imports---------------
import RPi.GPIO as GPIO
import os
import subprocess

# -----Bell specifics--------
BELL_PLAYER = 'omxplayer'
BELL_MP3 = 'bell-ring-01.mp3'
BELL_PLAY = BELL_PLAYER + ' -o local ' + BELL_MP3 + '&'

# -----Producer Specifics----
CLUSTER_HEADER = 'curl -X POST -H "Content-Type: application/vnd.kafka.json.v1+json" '
REMOTE_CLUSTER = 'http://54.193.3.192:8082/topics/topic1'
PRODUCE_PAYLOAD= """'{"records":[{"key":"Sarjeet", "value":"12M"}]}'"""
PRODUCE = CLUSTER_HEADER + '--data '+ PRODUCE_PAYLOAD + ' ' + REMOTE_CLUSTER

#------Continuous monitor while True: 

#----setup GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

#----set pin number 16 (GPIO23) set as input pin 
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#----check if pin has high voltage
input_high = 'Input high!'
input_low = 'Input low'
i = 0

#----detect vibration while loop
while i < 5:  
	GPIO.wait_for_edge(23, GPIO.RISING)
	print i
	print input_high
	i = i + 1
	GPIO.wait_for_edge(23, GPIO.FALLING)
	print input_low
	
#-----ring the bell	
legit_event = 'Legit event, Ring the Bell!'
print legit_event
os.system(BELL_PLAY);

#--------Produce to remote cluster------------------
print PRODUCE

subprocess.call([
	'sudo',
	'curl',
	'-X',
	'POST',
	'-H',
	'"Content-Type: application/vnd.kafka.json.v1 +json"',
	'--data',
	PRODUCE_PAYLOAD,
	REMOTE_CLUSTER
])

#os.system(PRODUCE)

GPIO.cleanup();

#-------Continuous monitor end of while
