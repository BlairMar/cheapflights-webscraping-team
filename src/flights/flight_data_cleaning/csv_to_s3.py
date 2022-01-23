#%%
import boto3
import os
import sys
sys.path.append(os.path.abspath('../flight_scraper'))

s3_resource = boto3.client('s3')

# my_bucket = s3_resource.Bucket(name='cheapflights-bucket')


def uploadDirectory(path,bucketname):
        for root,dirs,files in os.walk(path):
            for file in files:
                s3_resource.upload_file(os.path.join(root,file),bucketname, f"flights-data/{file}")
    
uploadDirectory('../flight_scraper/flights_information', 'cheapflights-bucket')


                

# %%
