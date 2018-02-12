#!/bin/bash
STR=$(date -d "last month" +"%y-%m")
mv /home/pi/temp.log /home/pi/$STR-temp.log
heirloom-mailx -a /home/pi/$STR-temp.log -s "monthly temperature log" youremail@gmail.com
#heirloom-mailx -a /home/pi/$STR-temp.log -s "monthly temperature log" another-email@gmail.com

