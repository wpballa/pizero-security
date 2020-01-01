#!/bin/bash
STR=$(date -d "last week" +"%y-%m")
mv /home/pi/temp.log /home/pi/$STR-temp.log
echo "monthly temperature log" | s-nail -a /home/pi/$STR-temp.log -s "monthly temperature log" youremail@gmail.com
#echo "monthly temperature log" | s-nail -a /home/pi/$STR-temp.log -s "monthly temperature log" another-email@gmail.com

