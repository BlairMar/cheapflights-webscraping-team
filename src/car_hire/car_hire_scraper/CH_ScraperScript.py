# %%
import sys
import os
sys.path.append(os.path.abspath('../'))
from CarScraper import *
import pandas as pd
import boto3

# Asks for user inputs for the data they would like to scrape.
'''

'''
city = input('Enter City that you would like Car Hire information for: ')
trip_start = input('Enter Start date of Journey in the format (YYYY-MM-DD): ')
trip_end = input('Enter End of Journey in the format (YYYY-MM-DD): ')
file = input('The data will be stored in an S3 Bucket, what would you like to name your Data file: ')

# Runs the scraper.
'''

'''
scraper = CarHireScraper()
CH_dataframe = scraper.scrape(city, trip_start, trip_end, False)

# Converts data into their respective type.
'''

'''
CH_dataframe['Number of Passengers'] = pd.to_numeric(CH_dataframe['Number of Passengers'])
CH_dataframe['Number of Passengers'] = CH_dataframe['Number of Passengers'].astype('Int64')
CH_dataframe['Total Price'] = CH_dataframe['Total Price'].astype('Int64')
CH_dataframe['Price'] = CH_dataframe['Price'].astype('Int64')

# Exports data to a csv file.
'''

'''
CH_dataframe.to_csv(f'{file}.csv', index=False)

# Sends data file to s3 bucket accessible by user.
'''

'''
folder = 'car-hire-user'
bucket = 'faizsbucket'
s3_bucket = boto3.resource('s3').Bucket(f'{bucket}')
s3_bucket.upload_file(f'{file}.csv', f'{folder}/{file}.csv')


print(f'Your file is available at xyz')
