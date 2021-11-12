# %%
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
from time import sleep
from selenium.webdriver.firefox.options import Options
import copy
from locators import *

# options = Options()
# options.headless = True

driver = webdriver.Firefox()

driver.get(url)

car_informations = driver.find_elements(By.XPATH, card)


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

def search_bar(search):
    cookie_clicker(cookie_button)
    sleep(2)
    try:
        bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, search))
        )
        bar = driver.find_element(By.XPATH, search)
        bar.click()
        typing = driver.find_element(By.XPATH, search_bar_typing)
        typing.send_keys('Paris')
        sleep(2)
        # typing.send_keys(Keys.ENTER)
        dropdown = driver.find_element(By.XPATH, drop_down)
        dropdown.click()
        button = driver.find_element(By.XPATH, search_button)
        button.click()

    except:
        print('Unable to find element')
        return

def date_period(trip_start, trip_end):
    sleep(5)
    print('Changing URL')
    current_url = driver.current_url
    list_url = current_url.split('/')
    list_url[-2] = trip_start
    end_date = list_url[-1]
    list_url[-1] = trip_end + end_date[10:]
    url = '/'.join(list_url)
    print(url)
    driver.get(url)
    print('URL Changed')
    sleep(5)

def car_card_main_info_scrape(car_information):

    search_bar(search_bar_path)
    date_period('2022-1-10', '2022-1-14')

    print('I am running')
    # sleep(5)
    # fake_click = driver.find_element(By.XPATH, faux_click)
    # fake_click.click()
    # print('Click')
    sleep(5)
    try:
        car_card_external_click = car_information.find_element(By.XPATH, car_card_external)
        car_card_external_click.click()
    except:
        car_card_click = car_information.find_element(By.XPATH, car_card)
        car_card_click.click()
    print('Click')
    sleep(5)

    car_info = copy.deepcopy(car_dict)

    for key in car_xpath_dict.keys():
        try:
            car_info[key] = car_information.find_element(By.XPATH, car_xpath_dict[key]).text
        except:
            continue
        
    # car_brand = driver.find_element(By.XPATH, car_type)
    # car_info['Car Type'] = car_brand.text

    # car_location = driver.find_element(By.XPATH, location)
    # car_info['Location'] = car_location.text

    # passenger_count = driver.find_element(By.XPATH, passengers)
    # car_info['Number of Passenger'] = passenger_count.text

    brands = car_information.find_elements(By.XPATH, brands_section)

    car_info['Brands'] = []

    for brand in brands:
        car_info['Brands'].append(car_card_sub_info_scrape(brand))

    return car_info


def car_card_sub_info_scrape(brand):

    brand_info = {}

    supplier_attribute = brand.find_element(By.XPATH, supplier_x)
    a = supplier_attribute.get_attribute('alt')
    supplier = a.split(': ')
    brand_info['Supplier'] = supplier[1]

    total_price_overall = brand.find_element(By.XPATH, total_price)
    brand_info['Total Price'] = total_price_overall.text

    ppday = brand.find_element(By.XPATH, pday)
    brand_info['Price'] = ppday.text

    offer = brand.find_element(By.XPATH, rate)
    brand_info['Offer Rating'] = offer.text

    return brand_info

    # car_info = copy.deepcopy(car_dict)
    # for key in car_xpath_dict.keys():
    #     try:
    #         car_info[key] = driver.find_element(By.XPATH, car_xpath_dict[key]).text
    #     except:
    #         continue
    # print(car_info)

    # # brand1 = copy.deepcopy(brand1_dict)
    # # for key in brand_dict.keys():
    # #     try:
    # #         brand1[key] = driver.find_element_by_xpath(brand_dict[key]).text
    # #     except:
    # #         continue
    # print(car_info)

for car_information in car_informations:
    car_card_main_info_scrape(car_information)


# # car_card_main_info_scrape(card)
# # print(all_car_information)


# %%
driver = webdriver.Firefox()

url = 'https://www.cheapflights.co.uk/cars/'

driver.get(url)

search_bar(search_bar_path)

sleep(5)
fake_click = driver.find_element(By.XPATH, faux_click)
fake_click.click()
sleep(5)
car_card_click = driver.find_element(By.XPATH, car_card)
car_card_click.click()
print('Click')
sleep(3)
deals = driver.find_element(By.XPATH, view_deal_button)
deals.click()
print('Click')
sleep(3)
# more = driver.find_element(By.XPATH, more_suppliers_button)
# more.click()
# print('Click')

car_brand = driver.find_element(By.XPATH, '//div[@class="MseY-title js-title"]')
print(car_brand.text)
car_location = driver.find_element(By.XPATH, '//div[@class="x9e3-address"]')
print(car_location.text)
passenger_count = driver.find_element(By.XPATH, '//div[@aria-label="Passengers count"]')
print(passenger_count.text)
supplier = driver.find_element(By.XPATH, '//div[@class="SB0e-Name"]')
print(supplier.text)
offer = driver.find_element(By.XPATH, '//div[@class="SB0e-Score"]')
print(offer.text)
total_price = driver.find_element(By.XPATH, '//div[@class="JwPH-totalPrice JwPH-mod-variant-specialRate"]')
print(total_price.text)
ppday = driver.find_element(By.XPATH, '//div[@class="JwPH-price"]')
print(ppday.text)


# %% Class
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from locators import *

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
    
    def search_bar(self, city):
        try:
            bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, search))
            )
            sleep(2)
            bar = self.driver.find_element(By.XPATH, search)
            bar.click()
            typing = self.driver.find_element(By.XPATH, search_bar_typing)
            typing.send_keys(city)
            sleep(2)
            dropdown = self.driver.find_element(By.XPATH, drop_down)
            dropdown.click()
            button = self.driver.find_element(By.XPATH, search_button)
            button.click()

        except:
            return print('Unable to find element')
            
Scraper = CarHireScraper()
Scraper.search_bar('London')
# %%




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
