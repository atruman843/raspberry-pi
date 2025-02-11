import json
import paho.mqtt.client as mqtt
from rpi_ws281x import *
import time
# from Lights.lights import Lights
# from AlarmClock.alarmClock import AlarmClock

actions = {}
# lights = Lights(5)
# alarmClock = AlarmClock()

def subscribe_to_topics():
  """
    Subscribe to all topics in this method. Topics are loaded from external 
    json file and have general structure of class.topic.action. Class defines 
    the device type. Topic defines the component/feature being configured:. Action
    defines the action taken when a message is received.
  """

  global actions

  with open('/home/pi/raspberry-pi/MQTTServer/topics.json') as f:
    topics = json.load(f)
  
  # define a list of topics to subscribe to and their respective actions
  for dest in topics:
      if topics[dest]:
        for dev in topics[dest]:
          if topics[dest][dev]:
            for param in topics[dest][dev]:
              # subscribe to the topic
              subscription = dest + "/" + dev + "/" + param
              print("Subscribing to: " + subscription)
              client.subscribe(subscription)

def on_connect(client, userdata, flags, rc):
  """
    Define what happens when a connection is established to the broker.
  """

  print("Connected with result code: {}".format(rc))

def on_message(client, userdata, message):
  """
    Define what happens when a message is received.
  """

  subscription = message.topic
  action_data  = message.payload
  print("Message received: {} - {}".format(subscription, action_data))

  # TODO
  # call the appropriate function
  subscription = subscription.replace("broker/", "", 1)
  client.publish(subscription, action_data)
  print("Sent message: {} with data: {}".format(subscription, action_data))

if __name__ == "__main__":

  # define and connect to the mqtt client
  client = mqtt.Client()
  client.connect("raspberrypi.local", 1883, 60)
  
  # after we connect, we must subscribe to all topics in our system
  subscribe_to_topics()

  # set what happens when you connect to the broker and when a message received
  client.on_connect = on_connect
  client.on_message = on_message

  # run the loop infinitely
  client.loop_forever()
