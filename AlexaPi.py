#Import all the libraries
import RPi.GPIO as GPIO
import time
from pubnub import Pubnub
 
# Initialize the Pubnub Keys 
pub_key = "pub-c-e72e7098-9da2-49c8-97a7-918c64abefac"
sub_key = "sub-c-48ff7940-8bd3-11e8-9c3a-c6a250b1bb88"
 
LIVING = 27            #define pin of RPi on which you want to take output
BR = 17 

def init():          #initalize the pubnub keys and start subscribing
 
 global pubnub    #Pubnub Initialization
 GPIO.setmode(GPIO.BCM)
 GPIO.setwarnings(False)
 GPIO.setup(LIVING,GPIO.OUT)
 GPIO.output(LIVING, False)
 GPIO.setup(BR,GPIO.OUT)
 GPIO.output(BR,False)
 pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key)
 pubnub.subscribe(channels='alexaTrigger', callback=callback, error=callback, reconnect=reconnect, disconnect=disconnect)
 
def control_alexa(controlCommand):          #this function control Alexa, commands received and action performed
 if(controlCommand.has_key("trigger")):
  if(controlCommand["trigger"] == "living" and controlCommand["status"] == 1):
   GPIO.output(LIVING, True) 
   print "Living room light is on"
  if(controlCommand["trigger"] == "living" and controlCommand["status"] == 0):
   GPIO.output(LIVING, False) 
   print "Living room light is off"
  if(controlCommand["trigger"] == "bedroom" and controlCommand["status"] == 1):
   GPIO.output(BR,True)
   print "Bedroom light is on"
  if(controlCommand["trigger"] == "bedroom" and controlCommand["status"] == 0):
   GPIO.output(BR,False)
   print "Bedroom light is off"
 else:
  pass


 
 
 
def callback(message, channel):        #this function waits for the message from the aleatrigger channel
 if(message.has_key("requester")):
  control_alexa(message)
 else:
  pass
 
 
def error(message):                    #if there is error in the channel,print the  error
 print("ERROR : " + str(message))
 
 
def reconnect(message):                #responds if server connects with pubnub
 print("RECONNECTED")
 
 
def disconnect(message):               #responds if server disconnects with pubnub
 print("DISCONNECTED")
 
 
if __name__ == '__main__':
 init()                    #Initialize the Script
