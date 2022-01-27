# %% Class
import sys
import os

from sqlalchemy import desc
sys.path.append(os.path.abspath('../'))
import pandas as pd
import copy
from Data.UploadTos3 import uploadDirectory
from locators import *
from concurrent import futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from tqdm.notebook import tqdm

class CarHireScraper:

    def __init__(self):
        pass
        

    def _cookie_click(self, cookie_button):
        '''
        Clicks the accept button when the cookies pop up appears.

        Parameters:
            xpath (str): String representation of the xpath for the cookies accept button.
        '''
        sleep(3)
        cookie = self.driver.find_element(By.XPATH, cookie_button)
        cookie.click()
        return True
    
    def _date_period(self, trip_start, trip_end):
        '''
        Changes the start and end date on the website.

        Parameters:
            dates (str): String representation of the date written Year-Month-Day.
        '''
        sleep(5)
        current_url = self.driver.current_url
        list_url = current_url.split('/')
        list_url[-2] = trip_start
        end_date = list_url[-1]
        list_url[-1] = trip_end + end_date[10:]
        url = '/'.join(list_url)
        self.driver.get(url)
        sleep(5)
        return url

    # Could be a staticmethod
    def destinations(self):
        '''
        Exracts the most popular cities to visit as determined by cheapflights.

        Returns:
            destination (list): List of popular city destinations.
        '''
        options = Options()
        # options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.get("https://www.cheapflights.co.uk/")
        self._cookie_click(cookie_button)
        destination = self.driver.find_elements(By.XPATH, destination_path)
        self.cities = [dest.text for dest in destination]
        self.driver.quit()
        return self.cities
    
    def _search_bar(self, search_bar_path, city):
        '''
        Finds and types within the search bar for your desired city.

        Parameters:
            city (str): String representation of the city you would like to hire a car.
        '''
        sleep(2)
        try:
            bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, search_bar_path))
            )
            bar = self.driver.find_element(By.XPATH, search_bar_path)
            bar.click()
            typing = self.driver.find_element(By.XPATH, search_bar_typing)
            typing.send_keys(city)
            sleep(2)
            dropdown = self.driver.find_element(By.XPATH, drop_down)
            dropdown.click()
            button = self.driver.find_element(By.XPATH, search_button)
            button.click()
            return True

        except:
            print('Unable to find element')
            return

    def _big_clicker(self):
        '''
        Clicks on each car card shown on the page.
        '''
        car_card_external_click = self.driver.find_elements(By.XPATH, car_card_external)
        for x in range(0, len(car_card_external_click)):
            if car_card_external_click[x].is_displayed():
                sleep(1)
                car_card_external_click[x].click()

        car_card_click = self.driver.find_elements(By.XPATH, car_card)
        for x in range(0, len(car_card_click)):
            if car_card_click[x].is_displayed():
                sleep(1)
                car_card_click[x].click()
        return True

    def _car_card_main_info_scrape(self, car_information, city):
        '''
        Scrapes the data of the Car name, Location and Number of Passengers.

        Parameters:
            xpath (str): String representation of the xpath for the card holding all the information.
        
        Returns:
            car_info (dict): Dictionary containing all the information for each car.
        '''

        sleep(5)

        car_info = copy.deepcopy(car_dict)

        car_info['City'] = city

        for key in car_xpath_dict.keys():
            try:
                car_info[key] = car_information.find_element(By.XPATH, car_xpath_dict[key]).text
            except:
                continue

        brands1 = car_information.find_elements(By.XPATH, brands_section)
      
        df = pd.DataFrame()

        for brand in brands1:
            car_info_copy = copy.deepcopy(car_info)
            car_info_copy.update(self._car_card_sub_info_scrape(brand))
            df = df.append(car_info_copy, ignore_index=True)

        return df

    def _car_card_sub_info_scrape(self, brand):
        '''
        Scrapes the data of the Supplier, Total Price, Price and Offer Rating.

        Parameters:
            xpath (str): String representation of the xpath for the card holding all the information.
        
        Returns:
            brand_info(dict): Dictionary containing all the information for each supplier for each car.
        '''

        brand_info = {}

        supplier_attribute = brand.find_element(By.XPATH, supplier_x)
        a = supplier_attribute.get_attribute('alt')
        supplier = a.split(': ')
        brand_info['Supplier'] = str(supplier[1])

        try:
            total_price_overall1 = brand.find_element(By.XPATH, total_price).text
            tp1 = total_price_overall1[1:]
            brand_info['Total Price'] = int(tp1)
        except:
            try:
                total_price_overall2 = brand.find_element(By.XPATH, t_price).text
                tp2 = total_price_overall2[1:]
                brand_info['Total Price'] = int(tp2)
            except:
                total_price_overall3 = brand.find_element(By.XPATH, total_price).text
                tp3 = total_price_overall3[1:].replace(",", "")
                brand_info['Total Price'] = int(tp3)

        ppday = brand.find_element(By.XPATH, pday).text
        size = len(ppday)
        price_per_day = ppday[1:size - 4]
        brand_info['Price'] = int(price_per_day)

        offer = brand.find_element(By.XPATH, rate).text
        brand_info['Offer Rating'] = float(offer)

        return brand_info

    def scrape(self, city, trip_start='2022-02-10', trip_end='2022-02-14', save=True):
        '''
        Runs all the methods to scrape a page of data.

        Parameters:
            xpath (str): String representation of the city you would like to hire a car.
        '''
        options = Options()
        # options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(url)
        try:
            self._cookie_click(cookie_button)
        except:
            pass
        self._search_bar(search_bar_path, city)
        self._date_period(trip_start, trip_end)

        sleep(20)
        
        try:
                    
            self._big_clicker()

            sleep(10)

            car_informations = self.driver.find_elements(By.XPATH, card)

            df_main = pd.DataFrame()

            for car_information in tqdm(car_informations, desc=f'{city}'):
                df = self._car_card_main_info_scrape(car_information, city)
                df_main = df_main.append(df, ignore_index=True)

            if save == True:
                df_main.to_csv(f'./Data/Car_Hire_Data/{city}_carhire.csv', index=False)
            else:
                pass
            
            self.driver.quit()

            return df_main

        except Exception:

            print(f'Stale Element found when scaping data for {city}')
            self.driver.quit()
            self.scrape(city)
        
        return

def threader(city):
    '''
        Defines the list of cities to cycle through for the multithreading.
    '''
    Scraper = CarHireScraper()
    Scraper.scrape(city)

def run():
    '''
        Runs the multithreading for the scraper using a list of cities.
    '''
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(threader, city)
                for city in pop_cities
            ]
        uploadDirectory('./Car_Hire_Data', 'faizsbucket')
    except Exception:
        pass

if __name__ == '__main__':
    run()
    # Scraper = CarHireScraper()
    # Scraper.scrape('London')

# %%
