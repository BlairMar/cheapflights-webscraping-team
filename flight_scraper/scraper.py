#%%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import COOKIES_POPUP, DESTINATIONS
from time import sleep
import logging
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

class FlightScraper:
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
    logging = logging.getLogger(f'flightscraper-scraper')
    
    def __init__(self) -> None:
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                             OperatingSystem.LINUX.value,
                             OperatingSystem.MAC_OS_X.value]
        user_agent_rotator = UserAgent(software_names=software_names,
                                       operating_systems=operating_systems,
                                       limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        options = Options()
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.cheapflights.co.uk/flight-search/AMS-BRS/2021-11-18/2021-11-25?sort=bestflight_a")
        self.__bypass_cookies()

    def __bypass_cookies(self) -> None:
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, COOKIES_POPUP))
            )
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, COOKIES_POPUP))
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
    
    def change_url(self, depart_date: str, return_date: str) -> None:
        curr_url = self.driver.current_url
        url_sections = curr_url.split('/')
        url_sections[-2] = depart_date
        return_section = url_sections[-1].split('?')
        return_section[0] = return_date
        url_sections[-1] = '?'.join(return_section)
        new_url = '/'.join(url_sections)
        self.driver.get(new_url)
        
    
scraper = FlightScraper()
scraper.change_url('2022-1-10', '2022-1-14')

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
