from Hotels_Scrape import Hotel_Scraper 
from Data_to_S3 import uploadDirectory
import pandas as pd
import re 
import boto3
import os

city = input('Enter City that you would like Top hotels for: ')
start_date = input('Enter Start date of Journey in the format (YYYY-MM-DD): ')
end_date = input('Enter End of Journey in the format (YYYY-MM-DD): ')
photos_indicator = input('Enter Yes/No if you would like photos of the hotels: ')
number_of_hotels = input('Enter Number of hotels to be scraped: ')
folder_name = input('The data will be stored in an S3 Bucket, what would you like to name the Folder: ')

if photos_indicator == "Yes":
    photo_ind = 1
else:
    photo_ind = 0

scraper = Hotel_Scraper()
hotel_data = scraper.hotels_in_city_scraper(city, start_date, end_date, photos=photo_ind, num_hotels=int(number_of_hotels), save=True)
hotel_data = scraper.clean_data(hotel_data)
       
uploadDirectory(city, folder_name)