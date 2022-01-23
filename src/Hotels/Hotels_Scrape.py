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


    def get_cities(self):
        """
        Given an xpath of the tags of popular cities, returns these cities. 

        Parameters:
            xpath (str): String representation of xpath for the tag containing the 
                        city information. 
            
        Returns:
            city_names (List): List of strings of popular city names. 
        
        
        """
        city_names = []
        cities = self.driver.find_elements(By.XPATH, cities_path)
        for city in cities:
            city_names.append(city.text)
        
        self.driver.quit()

        self.cities = city_names 

        return city_names
    


    def search_city(self, xpath):
        """
        Given a city, we search for this city on Cheapflights. 

        Parameters:
            city_name (str): City we want to find hotels in. 
            xpath (str): Xpath of the HTML element for searching cities. 
        
        Returns:
            None 

        """

        city_box = self.click(xpath)
        self.driver.execute_script("arguments[0].click();", city_box)
        sleep(10)
        city_box.send_keys(Keys.RETURN)
        sleep(3)


    def url_date_changer(self, start_date,end_date, city):
        """
        Change the Search parameters to look for hotels in a set period by changing
        the URL, then use driver to fetch this new page.  

        Parameters: 
            start_date (str): String representation of start date: YYYY-MM-DD
            end_date (str): String representation of end date: YYYY-MM-DD

        Returns:
            None
        
        """

        current_url = self.driver.current_url
        split_url = current_url.split('/')
        split_url[-2] = end_date
        split_url[-3] = start_date
        split_url[-4] = city
        url = '/'.join(split_url)
        self.driver.get(url)


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
        self.driver = webdriver.Chrome(options=self.options)

        self.driver.get(f'https://www.cheapflights.co.uk/hotels/{city_name}/{start_date}/{end_date}/2adults?sort=rank_a')

        self.driver.set_window_size(1200,1200)

        sleep(3)

        try:
            self.click(accept_cookies)
        except:
            pass

        sleep(20)

        hotels_information = pd.DataFrame()

        hotels = self.driver.find_elements(By.XPATH, hotel_results)
        hotel_results_page = self.driver.window_handles[0]
        for hotel in hotels[0:min(len(hotels), num_hotels)]: 
            hotel.click()
            tabs = self.driver.window_handles
            sleep(4)
            self.driver.switch_to.window(tabs[1-tabs.index(hotel_results_page)])
            hotel_info = self.hotel_page_scrape(city_name)
            hotel_name = self.driver.find_element_by_xpath(hotel_name_xpath).text
            hotels_information = hotels_information.append(hotel_info,ignore_index=True)
            if photos:
                self.get_hotel_photos(city_name, hotel_name)
        

            self.driver.close()
            self.driver.switch_to.window(hotel_results_page)

        self.driver.quit()


        """
            # Get Hotel Pictures:
            images = self.driver.find_elements(By.XPATH, images_xpath)
            attributes = [pic.get_attribute('style') for pic in images]
            pattern = re.compile('\([^)]+\)')
            url_ends = [url[2:-2] for url in [pattern.search(attribute)[0] for attribute in attributes]]
            for idx, url in enumerate(url_ends):
                image_url = cheap_flights_url + url
                directory = f'./Cleaned_Data/{city_name}/Hotel_Pictures/{hotel_name}'
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                urllib.request.urlretrieve(image_url, f'./Cleaned_Data/{city_name}/Hotel_Pictures/{hotel_name}/{hotel_name}_{idx}.jpg')
        """

        if save:
            hotels_information.to_csv(f'./Raw_Data/{city_name}.csv',index=False)
            cleaned_data = self.clean_data(hotels_information)
            cleaned_data.to_csv(f'./Cleaned_Data/{city_name}/{city_name}.csv', index=False)
            cleaned_data.to_csv(f'./Cleaned_CSVs/{city_name}.csv', index=False)

        return hotels_information

    
    def _number_finder(self, string):
        pattern = r'[0-9]*,?[0-9]+'
        value = re.compile(pattern)
        try: 
            return value.search(string)[0]
        except:
            return pd.NA

    def clean_data(self, df): 
        # Clean Data:

        #Below uses regular expressions to extract the cost of stay, an example uncleaned would be: £449total, cleaned would be: 449
        df['Cost of Stay'] = df['Cost of Stay'].apply(lambda cost: self._number_finder(cost))
        df['Number of Reviews'] = df['Number of Reviews'].apply(lambda review: self._number_finder(review))
        return df 


    def scrape_all_info(self, start_date, end_date):
        """
        Calling this function will scrape the top 20 hotels' information from all the popular cities,
        and store the information for each city within a CSV file in the "Hotels Information" directory. 
        """

        missing = ['Bali', 'Bangkok', 'Dalaman', 'Las Vegas', 'Murcia', 'Belfast']
        for city in missing:
            self.hotels_in_city_scraper(city, start_date, end_date, save=True)


def thread(city_name, start_date, end_date):
    scraper = Hotel_Scraper()
    scraper.hotels_in_city_scraper(city_name, start_date, end_date, save=True)


def scrape_data(start_date, end_date):
    func = lambda city: thread(city, start_date, end_date, save=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(func, city) for city in cities]
        #executor.map(func,cities)



if __name__ == '__main__':

    scraper = Hotel_Scraper()
    #scraper.hotels_in_city_scraper('Barcelona','2022-02-10','2022-02-14',save=True)
    scraper.scrape_all_info('2022-02-10', '2022-02-14')


# %%

# %%
