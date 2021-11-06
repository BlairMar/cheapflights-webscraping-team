#%%
import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from XPaths import *

# Access Cheap Flights Website:

driver = webdriver.Safari()

driver.get('https://www.cheapflights.co.uk')

def click(xpath):
    button = driver.find_element_by_xpath(xpath)
    button.click()
    sleep(3)
    return button

def get_cities(xpath):
    city_names = []
    cities = driver.find_elements(By.XPATH, xpath)
    for city in cities:
        city_names.append(city.text)
    return city_names

def dates_input(xpath):
    date_buttons = driver.find_elements(By.XPATH, xpath)
    driver.execute_script("arguments[0].innerText = 'Mon 10/1'", date_buttons[0])
    driver.execute_script("arguments[0].innerText = 'Fri 14/1'", date_buttons[1])
    sleep(3)

def search_city(xpath, city_name):
    city_box = click(xpath)
    city_box.send_keys(city_name)
    city_box.send_keys(Keys.RETURN)
    sleep(3)

try: 
    sleep(2)
    click(accept_xpath)
    locations = get_cities(cities_xpath)
    print(locations)
    click(stays_xpath)
    search_city(hotels_search_xpath,'Barcelona')
    dates_input(dates_xpath)
    driver.quit()
except Exception as e:
    print(e)
    driver.quit()
# %%
