#%% 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd 
import copy
from time import sleep
from XPaths import *
import concurrent.futures
import threading 
import urllib.request
import os 
import re 
from tqdm import tqdm

class Hotel_Scraper:
    def __init__(self):
        self.options = Options()
        #self.options.add_argument("--headless")
        self.options.add_argument("window-size=1400,1500")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("start-maximized")
        self.options.add_argument("enable-automation")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-dev-shm-usage")


    def click(self, xpath):
        """
        Give an xpath, that corresponds to a clickable html element, we click it.

        Parameters:
            xpath (str): String representation of xpath of element. 

        Returns:
            None
        
        """
        button = self.driver.find_element_by_xpath(xpath)
        button.click()
        sleep(3)
        return button


    def hotel_page_scrape(self, city_name):
        """
        The driver will already be loaded onto the page of a particular hotel, calling this function, will scrape the required data for this particular hotel. 

        Parameters:
            xpaths (List, xpaths[i] : str) : A list of xpaths of the information we want to scrape. Some of the key information for the hotel includes: 
                                            Name, Address, Average Rating, Number of reviews, Cheapest cost of stay and which provider offers this price. 
        
        Returns:
            info (dictionary): A dictionary, keys will be the category of the information we are looking for, and values will be the specific information for this hotel. 
        
        
        
        """
        info = copy.deepcopy(info_dict)
        info['City'] = city_name
        for key in xpath_dict.keys():
            try:
                info[key] = self.driver.find_element_by_xpath(xpath_dict[key]).text.replace('\n','')
            except:
                continue
        return info 

    
    def get_hotel_photos(self, city_name, hotel_name):
        """
        Provided the webdriver is on a page of a hotel. Provided the city name and hotel name, the photos are downloaded and saved locally. 

        Parameters:
            city_name(str): City Name

            hotel_name(str): Name of hotel. 
        

        Return:
            None: Photos are downloaded. 
        
        """

        images = self.driver.find_elements(By.XPATH, images_xpath)
        attributes = [pic.get_attribute('style') for pic in images]
        pattern = re.compile('\([^)]+\)')
        url_ends = [url[2:-2] for url in [pattern.search(attribute)[0] for attribute in attributes]]
        for idx, url in enumerate(url_ends):
            image_url = cheap_flights_url + url
            directory = f'./Cleaned_Data/{city_name}/Hotel_Pictures/{hotel_name}'
            if not os.path.isdir(directory):
                os.makedirs(directory)
            try:
                urllib.request.urlretrieve(image_url, f'./Cleaned_Data/{city_name}/Hotel_Pictures/{hotel_name}/{hotel_name}_{idx+1}.jpg')
            except:
                pass 


    def hotels_in_city_scraper(self, city_name, start_date, end_date, num_hotels=20, save=True, photos=True):
        """
        An instance of a driver will be created, the driver will load the cheapflights website, 
        click the cookies, enter the "Stays" page, edit the search parameters with the city_name
        provided. Then scrape the information from the first 10 hotels on this webpage.


        Parameters: 
            city_name (str): String represenation of the city whose hotels have been
                            loaded onto the driver. 
            start_date (str): Date in the format: YYYY-MM-DD, used to decide the start of date of the trip. 

            end_date (str): Date in the format: YYYY-MM-DD, end date of the trip. 

            save (Boolean): Keyword argument, set to True, if set to false, then we won't save the data into a CSV, only return the dataframe. 
        
        Returns:
            hotels_information (Pandas Dataframe): A dataframe of the information for
                            the hotels in this city. 
        

        """
        print("Initialising Scraper...")
        self.driver = webdriver.Chrome(options=self.options)

        self.driver.get(f'https://www.cheapflights.co.uk/hotels/{city_name}/{start_date}/{end_date}/2adults?sort=rank_a')

        self.driver.set_window_size(1200,1200)

        sleep(3)

        try:
            self.click(accept_cookies)
        except:
            pass

        print('Loading Webpage...')

        sleep(20)

        hotels_information = pd.DataFrame()

        hotels = self.driver.find_elements(By.XPATH, hotel_results)
        hotel_results_page = self.driver.window_handles[0]
        for hotel in tqdm(hotels[0:min(len(hotels), num_hotels)], desc=f'Scraping - {city_name}'): 
            hotel.click()
            tabs = self.driver.window_handles
            sleep(4)
            self.driver.switch_to.window(tabs[1-tabs.index(hotel_results_page)])
            hotel_info_dict = self.hotel_page_scrape(city_name)
            hotel_info = pd.DataFrame(hotel_info_dict, index=[0])
            hotel_name = self.driver.find_element_by_xpath(hotel_name_xpath).text
            hotels_information = pd.concat([hotels_information, hotel_info], ignore_index=True)
            if photos:
                self.get_hotel_photos(city_name, hotel_name)
        

            self.driver.close()
            self.driver.switch_to.window(hotel_results_page)

        self.driver.quit()

        if save:
            hotels_information.to_csv(f'./Raw_Data/{city_name}.csv',index=False)
            cleaned_data = self.clean_data(hotels_information)
            cleaned_data.to_csv(f'./Cleaned_Data/{city_name}/{city_name}.csv', index=False)
            cleaned_data.to_csv(f'./Cleaned_CSVs/{city_name}.csv', index=False)

        return hotels_information

    
    def _number_finder(self, param):
        """
        This method uses regular expressions to extract numbers from the string given. 

        Parameters:
            param (str/double): String/Double from which we want to extract numbers. 
        
        Returns: 
            number(str): String representation of the number extracted. Returns NULL in the event that no number is found. 
        
        """
        pattern = r'[0-9]*,?[0-9]+'
        value = re.compile(pattern)
        try:
            if isinstance(param, str):
                number_string = value.search(param)[0]
                number = number_string.replace(',','')
                return int(number)
            else:
                return int(param)
        except:
            return pd.NA


    def clean_data(self, df):
        """
        Cleans the dataframe of the Hotels Data. In particular the:  Number of Reviews/Cost/Rating are extracted and stored as real numbers. 

        Parameters:
            df (Pandas Dataframe): Dataframe of Hotels data that needs to be cleaned.

        Returns: 
            df (Pandas Dataframe): Cleaned Dataframe of Hotels data. 
        
        """

        #Below uses regular expressions to extract the cost of stay, an example uncleaned would be: £449total, cleaned would be: 449
        df['Cost of Stay'] = df['Cost of Stay'].apply(lambda cost: self._number_finder(cost))
        df['Number of Reviews'] = df['Number of Reviews'].apply(lambda review: self._number_finder(review))
        return df 


    def scrape_all_info(self, start_date, end_date):
        """
        Calling this function will scrape the top 20 hotels' information from all the popular cities,
        and store the information for each city within a CSV file in the "Hotels Information" directory. 

        Parameters:
            start_date (str): Date in the format: YYYY-MM-DD, used to decide the start of date of the trip. 

            end_date (str): Date in the format: YYYY-MM-DD, end date of the trip. 

        Return:
            None: Saves all CSVs and Photos into the folder "Cleaned_Data". 

        """

        for city in cities:
            self.hotels_in_city_scraper(city, start_date, end_date, save=True)


def thread(city_name, start_date, end_date):
    """
    Method used for Multithreading. Calling this method creates an instance of the scraper and scrapes data for the city and dates provided. 

    Parameters:
        city_name (str): String representation of the city.
        
        start_date (str): Date in the format: YYYY-MM-DD, used to decide the start of date of the trip. 

        end_date (str): Date in the format: YYYY-MM-DD, end date of the trip. 

    Return: 
        None: Saves Data into the folder "Cleaned_Data". 
    
    """
    scraper = Hotel_Scraper()
    scraper.hotels_in_city_scraper(city_name, start_date, end_date, save=True)


def scrape_data(start_date, end_date):
    """
    Function for Multithreading, scrapes all data concurrently. 

    Parameters:
        start_date (str): Date in the format: YYYY-MM-DD, used to decide the start of date of the trip. 

        end_date (str): Date in the format: YYYY-MM-DD, end date of the trip. 
    
    Return: 
        None: Saves all data into "Cleaned Data" folder. 
    
    """

    func = lambda city: thread(city, start_date, end_date, save=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(func, city) for city in cities]



if __name__ == '__main__':
    scraper = Hotel_Scraper()
    scraper.scrape_all_info('2022-02-10', '2022-02-14')


# %%
