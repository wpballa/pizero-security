#! /usr/bin/python3

# Python program to monitor water sensor and send mail if liquid is detected
# Use gpiozero V1.4 library for simplicity
# Dry sensor is low V, wet sensor is high V (~Vcc/2), but line, 
# no_line appear reversed who knows why
# Bill Ballard August 2017

from gpiozero import LED, LineSensor
import os
import time

# initialization

red = LED(10)
green = LED(11)
sensor = LineSensor(9, threshold=0.2, sample_rate=1.0)

# customize these next two lines for your application
# if you need to send multiple emails, simply add to this list
# here are the email addresses for text messages
# AT&T: [number]@txt.att.net
# Sprint: [number]@messaging.sprintpcs.com or [number]@pm.sprint.com
# T-Mobile: [number]@tmomail.net
# Verizon: [number]@vtext.com
# Boost Mobile: [number]@myboostmobile.com
# Cricket: [number]@sms.mycricket.com
# Metro PCS: [number]@mymetropcs.com
# Tracfone: [number]@mmst5.tracfone.com
# U.S. Cellular: [number]@email.uscc.net
# Virgin Mobile: [number]@vmobl.com
email = ["youremail@gmail.com", "anotheremail@comcast.net"]
loc = "Location"

# let them know code started

init = "echo " + time.ctime()
init = init + " | heirloom-mailx -s '" + loc + " water detector started' "

for addr in email:
    outs = init + addr
    os.system(outs)

wet = " | heirloom-mailx -s '" + loc + " water detected' "
dry = " | heirloom-mailx -s '" + loc + " no water detected' "

# function definitions

def WET():
# high line
    green.off()
    red.on()
    for addr in email:
        outs = "echo " + time.ctime() + wet + addr
        os.system(outs)

def DRY():
# low line
    green.on()
    red.off()
    for addr in email:
        outs = "echo " + time.ctime() + dry + addr
        os.system(outs)

# assume dry when installed

green.on()
red.off()

# infinite loop
while True:
    sensor.when_no_line = lambda: WET()
    sensor.when_line = lambda: DRY()
