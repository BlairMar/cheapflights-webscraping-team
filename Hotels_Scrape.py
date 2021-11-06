#%%
import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

# Access Cheap Flights Website:

driver = webdriver.Safari()

driver.get('https://www.cheapflights.co.uk')

accept_xpath = '//*[@title="Accept"]'

def click(xpath):
    button = driver.find_element_by_xpath(xpath)
    button.click()
    sleep(3)
    return button

cities_xpath = '//div[@class="Common-Layout-Brands-Cheapflights-DynamicLinks popularMapDestinations"]//ul/li/a/span[@class="linkText"]'

def get_cities(xpath):
    city_names = []
    cities = driver.find_elements(By.XPATH, xpath)
    for city in cities:
        city_names.append(city.text)
    return city_names

stays_xpath = '//a[@aria-label="Search for hotels"]'

hotels_search_xpath = '//div[@role="textbox"]//div[@class="lNCO-inner"]'

dates_xpath = '//span[@class="cQtq-value"]'

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