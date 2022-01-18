#!/bin/bash
export DISPLAY=:20 && 
Xvfb :20 -screen 0 1366x768x16 &&
python3 flight_scraper/flight_scraper_main.py

