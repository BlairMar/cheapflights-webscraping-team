#%%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import COOKIES_POPUP, DESTINATIONS, DEPARTURE_BUTTON, ORIGIN_TEXT_BOX


class FlightScraper:
    def __init__(self) -> None:
        # options = Options()
        # options.headless = True
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.cheapflights.co.uk/")
        self.__bypass_cookies()

    def __bypass_cookies(self) -> None:
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, COOKIES_POPUP))
            )
        except Exception as e:
            print(e)
        finally:
            cookie = self.driver.find_element(By.XPATH, COOKIES_POPUP)
            cookie.click()
    
    def get_popular_destinations(self) -> list:
        dest = self.driver.find_elements(By.XPATH, DESTINATIONS)
        popular_destinations = [element.text for element in dest]
        return popular_destinations
    
    def type_origin_search(self) -> None:
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(DEPARTURE_BUTTON))
            # WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(By.XPATH, DESTINATION_BUTTON))
        except Exception as e:
            print(e)
        finally:
            remove_origin = self.driver.find_element(By.XPATH, DEPARTURE_BUTTON)
            # remove_destination = self.driver.find_element(By.XPATH, DESTINATION_BUTTON)
            remove_origin.click()
            WebDriverWait(self.driver, 10).until((EC.element_to_be_clickable(ORIGIN_TEXT_BOX)))
            text_box = self.driver.find_element(By.XPATH, ORIGIN_TEXT_BOX)
            text_box.click()
            text_box.send_keys('Amsterdam')
            text_box.send_keys(Keys.RETURN)
            # remove_destination.click()

scraper = FlightScraper()
scraper.type_origin_search()


# chrome = webdriver.Chrome()
# chrome.get('https://www.cheapflights.co.uk/')
# link_element = 'span[class="linkText"]'
# dest_path = '//div[@class="Common-Layout-Brands-Cheapflights-DynamicLinks popularMapDestinations"]//ul/li/a/span[@class="linkText"]'
# cookies_button = '//button[@title="Accept"]'
# def bypass_cookies(button):
#     sleep(2)
#     cookie = chrome.find_element(By.XPATH, button)
#     return cookie.click()

# def popular_destinations(list):
#     bypass_cookies(cookies_button)
#     dest = chrome.find_elements(By.XPATH, list)
#     popular_destinations = [element.text for element in dest]
#     chrome.quit()
#     return popular_destinations

# popular_destinations(dest_path)


# %%
