import os
from pathlib import Path

from flight_scraper.flight_scraper_main import FlightScraper

city = input('Enter City that you would like top flights for: ')
trip_start = input('Enter Start date of Journey in the format (YYYY-MM-DD): ')
trip_end = input('Enter End of Journey in the format (YYYY-MM-DD): ')
# file = input('The data will be stored in an S3 Bucket, what would you like to name your Data file: ')

if Path(f"{os.getcwd()}/flight_scraper/flights_information/{city}_flights.csv").exists() == False:
    scraper = FlightScraper(city)
    scraper.scrape(trip_start, trip_end)