#! /bin/sh 

export DISPLAY=:20
Xvfb :20 -screen 0 1366x768x16 &
mkdir Cleaned_Data
mkdir Raw_Data
mkdir Cleaned_CSVs
python3 Hotels_Scraper/Data_Scraper_Script.py