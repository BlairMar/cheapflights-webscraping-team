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
    """
    Give an xpath, that corresponds to a clickable html element, we click it.

    Parameters:
        xpath (str): String representation of xpath of element. 

    Returns:
        None
    
    """
    button = driver.find_element_by_xpath(xpath)
    button.click()
    sleep(3)
    return button
    

def get_cities(xpath):
    """
    Given an xpath of the tags of popular cities, returns these cities. 

    Parameters:
        xpath (str): String representation of xpath for the tag containing the 
                     city information. 
        
    Returns:
        city_names (List): List of strings of popular city names. 
    
    
    """
    city_names = []
    cities = driver.find_elements(By.XPATH, xpath)
    for city in cities:
        city_names.append(city.text)
    return city_names


def dates_input(xpath):
    """
    Sets the start date for the holiday as 10/1/22, and end date as 14/1/22.

    Parameters: 
        xpath (str): xpath of the date box. 

    Returns:
        None
    
    """

    date_buttons = driver.find_elements(By.XPATH, xpath)
    driver.execute_script("arguments[0].innerText = 'Mon 10/1'", date_buttons[0])
    driver.execute_script("arguments[0].innerText = 'Fri 14/1'", date_buttons[1])
    sleep(3)


def search_city(xpath, city_name):
    """
    Given a city, we search for this city on Cheapflights. 

    Parameters:
        city_name (str): City we want to find hotels in. 
        xpath (str): Xpath of the HTML element for searching cities. 
    
    Returns:
        None 

    """
    city_box = click(xpath)
    city_box.send_keys(city_name)
    sleep(3)
    city_box.send_keys(Keys.RETURN)
    sleep(3)


def url_date_changer(start_date,end_date):
    """
    Change the Search parameters to look for hotels in a set period by changing
    the URL, then use driver to fetch this new page.  

    Parameters: 
        start_date (str): String representation of start date: YYYY-MM-DD
        end_date (str): String representation of end date: YYYY-MM-DD

    Returns:
        None
    
    """

    current_url = driver.current_url
    split_url = current_url.split('/')
    split_url[-2] = end_date
    split_url[-3] = start_date
    url = '/'.join(split_url)
    driver.get(url)

try: 
    sleep(2)
    driver.set_window_size(1200,1200)
    click(accept_cookies)
    locations = get_cities(cities)
    print(locations)
    click(stays)
    search_city(hotels_searchbox,'Barcelona')
    click(exit_datebox)
    click(search_button)
    sleep(5)
    url_date_changer('2022-01-10','2022-01-14')
    sleep(10)
    search_city(hotels_searchbox,'Las Vegas')
    click(search_button)
    
    driver.quit()
except Exception as e:
    print(e)
    driver.quit()
# %%
