import boto3
import os
from tqdm import tqdm

# Add Connection to S3 Bucket, to store our data. 
s3 = boto3.resource('s3')

def uploadDirectory(city,folder_name, bucketname='cheapflights-scraper-hotel-data'):
    s3_bucket = s3.Bucket(bucketname)
    for root,dirs,files in os.walk(f'./Cleaned_Data/{city}'):
        for file in files:
            file_type = file[-3:]
            if file_type == 'csv':
                s3_bucket.upload_file(os.path.join(root,file),f'{folder_name}/{file}')
            else:
                hotel_name = file.split('.')[0].replace('_',' ')[:-2]
                s3_bucket.upload_file(os.path.join(root,file),f'{folder_name}/Hotel Pictures/{hotel_name}/{file}')

