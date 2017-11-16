#! /usr/bin/python3

# Uses Adafruit PIR sensor to detect motion and send e-mail to a list of
# recipients. Also lets people know that the service is started.

from gpiozero import MotionSensor
import os
import time

# initialization, edit the name to be something meaningful and change the 
# list of emails to those that need notification

pirpin = 18
name = "Location"
email = ["your-email@gmail.com", "another-email@att.net"]
mailpart =  " | heirloom-mailx -s '" + name + " motion detected' "
mailstart = " | heirloom-mailx -s '" + name + " motion detector started' "
pir = MotionSensor(pirpin)

# function definitions

def MOT():
    for addr in email:
        outs = "echo " + name + " motion detected at "
        outs = outs + time.ctime() + mailpart + addr
        os.system(outs)
        print(outs)
def NOMOT():
    print("No Motion Detected")

# let them know it is started

for addr in email:
    outs = "echo " + name + " motion detection started at "
    outs = outs + time.ctime() + mailstart + addr
    os.system(outs)
    print(outs)

# loop looking for motion

while True:
    try:
        pir.when_motion = lambda: MOT()
        pir.when_no_motion = lambda: NOMOT()
    except (KeyboardInterrupt, SystemExit):
        break
