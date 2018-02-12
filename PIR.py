#! /usr/bin/python3

# uses a PIR sensor and gpiozero library to detect motion
# recommend setting PIR time constant on the board to long 
# to minimize multiple emails

from gpiozero import MotionSensor
import os
import time

# initialization

# customize these next two lines
email = ["youremail@gmail.com","anotheremail@comcast.net"]
loc = "Location"

mailpart =  " | heirloom-mailx -s '" + loc + " motion detected' "
mailstart = " | heirloom-mailx -s '" + loc + " motion detector started' "
pirpin = 14     # physical pin 8
pir = MotionSensor(pirpin)

# function definitions

def MOT():
    for addr in email:
        outs = "echo " + loc + " motion detected at " + time.ctime() + mailpart + addr
        os.system(outs)

def NOMOT():
    print("No Motion Detected")

# let them know it is started

for addr in email:
    outs = "echo " + loc + " motion detection started at " + time.ctime() + mailstart + addr
    os.system(outs)

# loop looking for motion

while True:
    try:
        pir.when_motion = lambda: MOT()
        pir.when_no_motion = lambda: NOMOT()
    except (KeyboardInterrupt, SystemExit):
        break
