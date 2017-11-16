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

red = LED(17)
green = LED(22)
sensor = LineSensor(27, threshold=0.2, sample_rate=1.0)

# give a good name so you will know where the alarm is coming from

name = "Location"

# if you need to send multiple emails, simply add to this list

email = ["youremail@gmail.com", "anotheremail@att.net"]

# let them know code started

init = "echo " + time.ctime()
init = init + " | heirloom-mailx -s '" + name + " liquid detector started' "

for addr in email:
    outs = init + addr
    os.system(outs)

wet = " | heirloom-mailx -s '" + name + " liquid detected' "
dry = " | heirloom-mailx -s '" + name + " no liquid detected' "

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
