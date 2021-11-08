# %%

import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
from time import sleep

driver = webdriver.Firefox()

url = "https://www.cheapflights.co.uk/cars/"

driver.get(url)

cookie_button = '//button[@title="Accept"]'
destination_path = '//ul/li/a/span[@class="linkText"]'


def cookie_clicker(button):
    sleep(3)
    cookie = driver.find_element(By.XPATH, button)
    return cookie.click()


def popular_destinations(list):
    cookie_clicker(cookie_button)
    destination = driver.find_elements(By.XPATH, list)
    return [dest.text for dest in destination]

def open_new_tab():
    # Open a new window
    # This does not change focus to the new window for the driver.
    driver.execute_script("window.open('');")
    sleep(3)
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    


# %% Tab Close
    driver.get("http://stackoverflow.com")
    sleep(3)
    # close the active tab
    driver.close()
    sleep(3)
    # Switch back to the first tab
    driver.switch_to.window(driver.window_handles[0])
    driver.get("http://google.se")
    sleep(3)
    # Close the only tab, will also close the browser.
    driver.close()



# %% Search Bar and Type Word

# search_bar_path = '/html/body/div[5]/div/div[2]/div[1]/div[2]/div/input'
search_bar_path = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[1]/div[1]/div/div'
search_bar_typing = '/html/body/div[5]/div/div[2]/div[1]/div[2]/div/input'
search_button = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[2]/button'
drop_down = '/html/body/div[5]/div/div[2]/div[2]/div/ul/li[2]/div/div[2]'

def search_bar(search):
    popular_destinations(destination_path)
    
    try:
        bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, search))
        )
        bar = driver.find_element(By.XPATH, search)
        bar.click()
        typing = driver.find_element(By.XPATH, search_bar_typing)
        typing.send_keys('London')
        sleep(2)
        # typing.send_keys(Keys.ENTER)
        dropdown = driver.find_element(By.XPATH, drop_down)
        dropdown.click()
        button = driver.find_element(By.XPATH, search_button)
        button.click()

    except:
        print('Unable to find element')
        return

search_bar(search_bar_path)


# %% Class
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class CarHireScraper:

    def __init__(self):
        self.firefox_options = webdriver.FirefoxOptions()
        self.firefox_options.add_argument('--start-maximized')
        self.driver = webdriver.Firefox(options=self.firefox_options)
        self.driver.maximize_window()
        self.driver.get("https://www.cheapflights.co.uk/cars/")
        try:
            self._cookie_click()
        except:
            pass

    def _cookie_click(self):
        sleep(3)
        cookie = self.driver.find_element(By.XPATH, '//button[@title="Accept"]')
        return cookie.click()
    
    def destinations(self):
        destination = driver.find_elements(By.XPATH, '//ul/li/a/span[@class="linkText"]')
        return [dest.text for dest in destination]
    
    def search_bar(self, location):
        try:
            bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[1]/div[1]/div/div'))
            )
            bar = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[1]/div[1]/div/div')
            bar.click()
            typing = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div[1]/div[2]/div/input')
            typing.send_keys(location)
            sleep(2)
            # typing.send_keys(Keys.ENTER)
            dropdown = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div[2]/div/ul/li[2]/div/div[2]')
            dropdown.click()
            button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[2]/button')
            button.click()

        except:
            return print('Unable to find element')
            
Scraper = CarHireScraper()
Scraper.search_bar('London')
# %%

