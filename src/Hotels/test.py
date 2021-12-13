
#%%
import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from XPaths import *
import copy 

def hotel_page_scrape():
    """
    The driver will already be loaded onto the page of a particular hotel, calling this function, will scrape the required data for this particular hotel. 

    Parameters:
        xpaths (List, xpaths[i] : str) : A list of xpaths of the information we want to scrape. Some of the key information for the hotel includes: 
                                        Name, Address, Average Rating, Number of reviews, Cheapest cost of stay and which provider offers this price. 
    
    Returns:
        info (dictionary): A dictionary, keys will be the category of the information we are looking for, and values will be the specific information for this hotel. 
    
    
    
    """
    info = copy.deepcopy(info_dict)
    for key in xpath_dict.keys():
        try:
            info[key] = driver.find_element_by_xpath(xpath_dict[key]).text
        except:
            continue
    return info 


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

driver = webdriver.Safari()
driver.get('https://www.cheapflights.co.uk/hotels/Barcelona,Catalonia,Spain-c22567/2022-01-10/2022-01-14/2adults?sort=rank_a')
driver.set_window_size(1200,1200)
sleep(20)    
click(accept_cookies)

hotel_results_page = driver.window_handles[0]

hotels = driver.find_elements(By.XPATH, hotel_results)
hotels[0].click()   

sleep(10)

chwd = driver.window_handles

driver.switch_to.window(chwd[1-chwd.index(hotel_results_page)])

print(hotel_page_scrape())

sleep(5)

driver.close()

driver.switch_to.window(hotel_results_page)

hotels[1].click()

sleep(10)

chwd = driver.window_handles

driver.switch_to.window(chwd[1-chwd.index(hotel_results_page)])

print(hotel_page_scrape())

driver.close()

driver.switch_to.window(hotel_results_page)

driver.quit()

# %%
