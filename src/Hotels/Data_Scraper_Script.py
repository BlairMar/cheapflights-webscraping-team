from Hotels_Scrape import Hotel_Scraper 
import pandas as pd
import re 
import boto3 

city = input('Enter City that you would like Top hotels for: ')
start_date = input('Enter Start date of Journey in the format (YYYY-MM-DD): ')
end_date = input('Enter End of Journey in the format (YYYY-MM-DD): ')
file_name = input('The data will be stored in an S3 Bucket, what would you like to name your Data file: ')

scraper = Hotel_Scraper()
hotel_data = scraper.hotels_in_city_scraper(city, start_date, end_date, save=False)
hotel_data = scraper.clean_data(hotel_data)

def clean_data(df): 
    # Clean Data:

    #Below uses regular expressions to extract the cost of stay, an example uncleaned would be: £449total, cleaned would be: 449
    pattern = r'[0-9]+,?[0-9]+'
    value = re.compile(pattern)
    df['Cost of Stay'] = df['Cost of Stay'].apply(lambda cost: value.search(cost)[0])

    #Drop the commas in number of reviews, and convert floats, then to integers. 
    """
    df['Number of Reviews'] = df['Number of Reviews'].str.replace(',','')
    df['Number of Reviews'] = pd.to_numeric(df['Number of Reviews']) 
    df['Number of Reviews'] = df['Number of Reviews'].astype('Int64')
    """
    df['Number of Reviews'] = df['Number of Reviews'].apply(lambda review: value.search(review)[0])

    return df 

print(hotel_data)

#Save Cleaned Data
hotel_data.to_csv(f'{file_name}.csv', index=False)


# Add Connection to S3 Bucket, to store our data. 
s3_bucket = boto3.resource('s3').Bucket('cheapflights-scraper-hotel-data')

s3_bucket.upload_file(f'{file_name}.csv', f'Hotels_Information/{file_name}.csv')





