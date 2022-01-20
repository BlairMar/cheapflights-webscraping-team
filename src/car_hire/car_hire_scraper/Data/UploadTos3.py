# %%
import boto3
import os
import sys


s3_resource = boto3.client('s3')

def uploadDirectory(path,bucketname):
        for root,dirs,files in os.walk(path):
            for file in files:
                s3_resource.upload_file(os.path.join(root,file),bucketname, f'car-hire-data/{file}')
    
uploadDirectory('./Car_Hire_Data', 'cheapflights-bucket')
# %%
