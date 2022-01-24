from Hotels_Scrape import Hotel_Scraper 
import pandas as pd
import re 
import boto3
import os
import sys

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

# Add Connection to S3 Bucket, to store our data. 
s3_bucket = boto3.client('s3')

def uploadDirectory(city,bucketname='cheapflights-scraper-hotel-data'):
    for root,dirs,files in os.walk(f'./Cleaned_Data/{city}'):
        for file in files:
            file_type = file[-3:]
            if file_type == 'csv':
                s3_bucket.upload_file(os.path.join(root,file),bucketname,f'{folder_name}/{file}')
            else:
                hotel_name = file.split('.')[0].replace('_',' ')[:-2]
                s3_bucket.upload_file(os.path.join(root,file),bucketname,f'{folder_name}/Hotel Pictures/{hotel_name}/{file}')

uploadDirectory(city)

#s3_bucket.upload_file(f'./Cleaned_Data/{city}', f'User_Hotels_Information/{folder_name}')
"""
import boto3
folder_name='Florence_data'
s3_bucket = boto3.client('s3')
for root,dirs,files in os.walk(f'./Cleaned_Data/Florence'):
    for file in files:
        file_type = file[-3:]
        if file_type == 'csv':
            s3_bucket.upload_file(os.path.join(root,file),'cheapflights-scraper-hotel-data',f'{folder_name}/{file}')
        else:
            hotel_name = file.split('.')[0].replace('_',' ')[:-2]
            s3_bucket.upload_file(os.path.join(root,file),'cheapflights-scraper-hotel-data',f'{folder_name}/Hotel Pictures/{hotel_name}/{file}')


"""
