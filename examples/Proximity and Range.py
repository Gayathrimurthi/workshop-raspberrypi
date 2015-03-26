#import Pubnub, GPIO and time libraries

from Pubnub import Pubnub
import RPi.GPIO as GPIO
import time
import sys

##------------------------------
## Set up PubNub
## Put in Pub/Sub and Secret keys (replace 'demo')
## Define your PubNub channel
##------------------------------

publish_key = len(sys.argv) > 1 and sys.argv[1] or 'demo'
subscribe_key = len(sys.argv) > 2 and sys.argv[2] or 'demo'
secret_key = len(sys.argv) > 3 and sys.argv[3] or 'demo'
cipher_key = len(sys.argv) > 4 and sys.argv[4] or ''
ssl_on = len(sys.argv) > 5 and bool(sys.argv[5]) or False

pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key,secret_key=secret_key, cipher_key=cipher_key, ssl_on=ssl_on)

##Define Pub and Sub channels. Pub channel can be anything; Sub channel must match that of the device you're listening to. 
channel = 'Rangefinder'
subchannel = 'MotionDetector'

##Define parameters PN will use to subscribe to another channel
##"Callback" is where you process the message, and it will hold most of our code.

# Asynchronous usage
def callback(submessage, channel):
    print(submessage)

    ##Check to see if motion has been detected##
    if submessage["motion"] == 1:

    ##If so, run Rangefinder code##
        print("Object detected! Distance Measurement in Progress")
        #Send a pulse for 10 microseconds.
        while True:
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

        #Instatiate a time stamp for when a signal is detected by setting beginning + end values.
        #Then subtract beginning from end to get duration value.

            print("before pulse start")
            pulse_start = time.time()
            while GPIO.input(ECHO)==0:
                #print("waiting for pulse signal")
                pulse_start = time.time()

            while GPIO.input(ECHO)==1:
                pulse_end = time.time()
            print("after pulse")
            pulse_duration = pulse_end - pulse_start

            ##Simplify + Flip it: distance = pulse_duration x 17150
            distance = pulse_duration*17150

        ##Round out distance for simplicity and print.

            distance = round(distance, 2)
            loopcount += 1
            print('shot #'+str(loopcount))

        ##Use the distance measurement as a proximity alarm.
        ##Set 'distance' in if-loop to desired alarm distance.
        ##When the alarm is tripped, the distance and a note are sent as a dictionary in a PubNub message, and the sensor stops searching.

            if distance <= 20:
                print("Distance:",distance,"cm")
                print("Proximity Detected")

                message = {'distance': distance, 'Proximity': 1}
                print pubnub.publish(channel = 'Rangefinder', message)
                time.sleep(1)


        ##If nothing is detected, the sensor continuously sends and listens for a signal, and publishes the distance to your PubNub channel.
            else:
                print("Time:", pulse_duration)
                print("Distance:", distance, "cm")
                print("Sorry, Too Far")

                message = {'distance': distance, 'Proximity' : 0}
                print pubnub.publish(channel= 'Rangefinder', message)

            time.sleep(1)

        #Clean up GPIO pins + reset
        GPIO.cleanup()
        sys.exit()
    else:
        print("Nothing detected.")

def error(message):
    print("ERROR : " + str(message))


def connect(message):
    print("CONNECTED")


def reconnect(message):
    print("RECONNECTED")


def disconnect(message):
    print("DISCONNECTED")


##Setup Rangefinder##
##  The code seems out of order, as the Rangefinder functionality has been typed above- before setting up the pins.##
##  But, that code can only be called upon receiving the proper message.##
##  Messages are only received after subscribing to a channel.##
##  That subscription happens at the end of this code.##
i = 0
loopcount = 0


#Set GPIO pins used on breadboard.

GPIO.setmode(GPIO.BCM)
TRIG = 20
ECHO = 26

GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)

#Settle the trigger and wait
GPIO.output(TRIG,False)
print("Waiting for sensor to settle.")

time.sleep(2)


##Actually subscribe to the channel to receive the messages:##
pubnub.subscribe(channel = subchannel, callback=callback, error=callback,
                 connect=connect, reconnect=reconnect, disconnect=disconnect)






