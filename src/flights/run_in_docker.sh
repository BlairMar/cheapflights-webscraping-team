#! /bin/sh 

export DISPLAY=:20
Xvfb :20 -screen 0 1366x768x16 &
python3 flights_script.py

