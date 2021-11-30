#%%
import requests 
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
import os 

class Hotel_Scraper:
    def __init__(self):
        #self.chrome_options = Options()
        #self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.cheapflights.co.uk')
        self.driver.set_window_size(1200,1200)
        sleep(5)
        self.click(accept_cookies)
        self.get_cities()
        self.all_hotels_info = pd.DataFrame()
        self.click_cookies = True


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
    


    def search_city(self, xpath, city_name):
        """
        Given a city, we search for this city on Cheapflights. 

        Parameters:
            city_name (str): City we want to find hotels in. 
            xpath (str): Xpath of the HTML element for searching cities. 
        
        Returns:
            None 

        """
        print('test')
        city_box = self.click(xpath)
        print('test_2')
        self.driver.execute_script("arguments[0].click();", city_box)
        #city_box.send_keys('hello')
        sleep(10)
        print('test_3')
        city_box.send_keys(Keys.RETURN)
        sleep(3)


    def url_date_changer(self, start_date,end_date):
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
                info[key] = self.driver.find_element_by_xpath(xpath_dict[key]).text
            except:
                continue
        return info 



    def hotels_in_city_scraper(self, city_name):
        """
        An instance of a driver will be created, the driver will load the cheapflights website, 
        click the cookies, enter the "Stays" page, edit the search parameters with the city_name
        provided. Then scrape the information from the first 10 hotels on this webpage.


        Parameters: 
            city_name (str): String represenation of the city whose hotels have been
                            loaded onto the driver. 
        
        Returns:
            hotels_information (Pandas Dataframe): A dataframe of the information for
                            the hotels in this city. 
        

        """
        self.driver = webdriver.Chrome()

        self.driver.get('https://www.cheapflights.co.uk/')
        self.driver.set_window_size(1200,1200)
        sleep(3)

        try:
            self.click(accept_cookies)
        except:
            pass

        
        self.click(stays)
        self.search_city(hotels_searchbox, city_name)
        self.click(exit_datebox)
        self.click(search_button)
        sleep(5)
        self.url_date_changer('2022-01-10','2022-01-14')
        sleep(30)

        current_handle = self.driver.current_window_handle
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1-tabs.index(current_handle)])
        self.driver.close()
        self.driver.switch_to.window(current_handle)


        hotels_information = pd.DataFrame()

        hotels = self.driver.find_elements(By.XPATH, hotel_results)
        hotel_results_page = self.driver.window_handles[0]
        for hotel in hotels[0:10]: 
            hotel.click()
            tabs = self.driver.window_handles
            sleep(8)
            self.driver.switch_to.window(tabs[1-tabs.index(hotel_results_page)])
            hotel_info = self.hotel_page_scrape(city_name)
            hotels_information = hotels_information.append(hotel_info,ignore_index=True)
            self.driver.close()
            self.driver.switch_to.window(hotel_results_page)

        print(city_name)

        self.city = city_name

        self.driver.quit()

        hotels_information.to_csv(f'./Hotels Information/{city_name}_2.csv',index=False)

        return hotels_information


    def scrape_all_info(self):
        """
        Calling this function will scrape the top 10 hotels' information from all the popular cities,
        and store the information for each city within a CSV file in the "Hotels Information" directory. 
        
        
        """
        for city in self.cities:
            city_hotels = self.hotels_in_city_scraper(city)
            city_hotels.to_csv(f'{os.getcwd()}/Hotels Information/{self.city}.csv',index=False)


    def scrape_all_futures(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            scrapers = [executor.submit(self.hotels_in_city_scraper,city) for city in self.cities]
        
            for scraper in scrapers:
                scraper.result()

    def scrape_all(self):

        thread_list = list()

        for city in self.cities[0:1]:
            scraper = threading.Thread(target=self.hotels_in_city_scraper, args=[city])
            scraper.start()
            thread_list.append(scraper)
        
        for thread in thread_list:
            thread.join()





if __name__ == '__main__':

    a = Hotel_Scraper()
    a.scrape_all()
    "data = a.hotels_in_city_scraper('Dalaman')"
    "data.to_csv('./Hotels Information/Dalaman.csv',index=False)"

# %%

# %%
