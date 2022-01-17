#! /bin/sh 

export DISPLAY=:20
Xvfb :20 -screen 0 1366x768x16 &
python3 Hotels_Scraper/Data_Scraper_Script.py