#Sensor digital Out
Connect to pin 16 (GPIO23) of raspbery pi 

#Play bell sound on audio 
omxplayer -o local  bell-ring-01.mp3 

#producer post:
curl -X POST -H "Content-Type: application/vnd.kafka.json.v1+json" --data '{"records":[{"key":"Sarjeet", "value":"12M"}]}' "http://54.193.3.192:8082/topics/topic1"

#Create Consumer instance:
curl -X POST -H "Content-Type: application/vnd.kafka.v1+json" --data '{"name":"consumer","format": "json", "auto.offset.reset": "earliest"}' http://54.193.3.192:8082/consumers/grp1
 
#Consume from topic:
curl -X GET -H "Accept: application/vnd.kafka.json.v1+json" http://54.193.3.192:8082/consumers/grp1/instances/consumer/topics/topic1

#Clean Consumer:
curl -X DELETE http://54.193.3.192:8082/consumers/grp1/instances/consumer
