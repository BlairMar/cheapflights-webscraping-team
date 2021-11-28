#%%
import os
import logging
import pandas as pd
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from locators import COOKIES_POPUP, FLIGHTS_MAIN, FLIGHTS_CARD, AIRLINE
from destination_codes import AIRPORT_CODES, DESTINATIONS

class FlightScraper:
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', 
                        level=logging.INFO,
                        filename='flight_scraper_logs.txt')
    logging = logging.getLogger(__name__)
    
    def __init__(self) -> None:
        logging.info('Initializing Scraper')
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                             OperatingSystem.LINUX.value,
                             OperatingSystem.MAC_OS_X.value]
        user_agent_rotator = UserAgent(software_names=software_names,
                                       operating_systems=operating_systems,
                                       limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        options = Options()
        options.add_argument('--disable-blink-features')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.headless = True
        options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": f"{user_agent}"})
        self.driver.get("https://www.cheapflights.co.uk/flight-search/LHR-AMS/2021-12-02/2021-12-05?sort=bestflight_a")
        self.__bypass_cookies()
        self.city = ""

    def __bypass_cookies(self) -> None:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, COOKIES_POPUP))
            )
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, COOKIES_POPUP))
            )
        except Exception as e:
            logging.error(f"{e}", exc_info=True)
        finally:
            cookie = self.driver.find_element(By.XPATH, COOKIES_POPUP)
            cookie.click()
    
    def change_url(self, depart_date: str, return_date: str, destination) -> None:
        curr_url = self.driver.current_url
        url_sections = curr_url.split('/')
        url_sections[-2] = depart_date
        logging.info(f'Depart date changed to {depart_date}')
        airports = url_sections[-3].split('-')
        airports[1] = destination
        url_sections[-3] = '-'.join(airports)
        logging.info(f'Destination changed to {destination}')
        return_section = url_sections[-1].split('?')
        return_section[0] = return_date
        logging.info(f'Return date changed to {return_date}')
        url_sections[-1] = '?'.join(return_section)
        new_url = '/'.join(url_sections)
        self.driver.get(new_url)
        self.city = destination
        return self.city
        
    def get_flight_info(self, info):
        flight = {}
        sleep(2)
        origin_container = info.find_elements(By.XPATH, FLIGHTS_MAIN)[0].text
        sleep(2)
        return_container = info.find_elements(By.XPATH, FLIGHTS_MAIN)[1].text
        sleep(2)
        airline = info.find_element(By.XPATH, AIRLINE).text
        flight['Origin-Flight'] = origin_container.split('\n')[0]
        flight['Origin-Airport'] = origin_container.split('\n')[1]
        flight['Airline'] = airline
        flight['Origin-Destination-Airport'] = origin_container.split('\n')[3]
        flight['Origin-Flight-Type'] = origin_container.split('\n')[4]
        flight['Origin-Flight-Duration'] = origin_container.split('\n')[5]
        flight['Return-Flight'] = return_container.split('\n')[0]
        flight['Return-Airport'] = return_container.split('\n')[1]
        flight['Return-Destination-Airport'] = return_container.split('\n')[3]
        flight['Return-Flight-Type'] = return_container.split('\n')[4]
        flight['Return-Flight-Duration'] = return_container.split('\n')[5]
        
        return flight
        
    def get_flight_info_driver(self) -> pd.DataFrame:
        try:
            logging.info('Getting information on flights')
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, FLIGHTS_CARD)))
        except Exception as e:
            logging.error(f'{e}', exc_info=True)
        else:
            sleep(5)
            self.driver.refresh()
            flights_info = self.driver.find_elements(By.XPATH, FLIGHTS_CARD)
            list_of_flight_dicts = []
            for info in tqdm(flights_info, desc="Flight info progress:", total=len(flights_info)):
                flight = self.get_flight_info(info)
                flights_df = pd.DataFrame([flight], columns=flight.keys())
                list_of_flight_dicts.append(flights_df)
            flights_df = pd.concat(list_of_flight_dicts)
            flights_df.to_csv(f'{os.getcwd()}/flights_information/{self.city}.csv', index=False)
            
            
    def scrape(self, depart_date, return_date, destination):
        self.change_url(depart_date, return_date, destination)
        self.get_flight_info_driver()

    
    def run(self):
        with ThreadPoolExecutor() as executor:
            scrapers = [
                executor.submit(
                    self.scrape, '2022-01-10', '2022-01-14', AIRPORT_CODES[city]) for city in tqdm(DESTINATIONS, desc='Scraper Progress', total=len(DESTINATIONS))
                                                                                                   ]
        for scraper in scrapers:
            scraper.result()
            
scraper = FlightScraper()
scraper.run()
# %%
