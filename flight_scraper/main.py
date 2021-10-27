#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

chrome = webdriver.Chrome()
chrome.get('https://www.cheapflights.co.uk/')
link_element = 'span[class="linkText"]'
dest_path = '//div[@class="Common-Layout-Brands-Cheapflights-DynamicLinks popularMapDestinations"]//ul/li/a/span[@class="linkText"]'
cookies_button = '//button[@title="Accept"]'
def bypass_cookies(button):
    sleep(2)
    cookie = chrome.find_element(By.XPATH, button)
    return cookie.click()

def popular_destinations(list):
    bypass_cookies(cookies_button)
    dest = chrome.find_elements(By.XPATH, list)
    popular_destinations = [element.text for element in dest]
    chrome.quit()
    return popular_destinations
    
popular_destinations(dest_path)
# %%
