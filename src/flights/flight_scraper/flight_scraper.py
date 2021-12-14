#%%
import os
import logging
import queue
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from locators import LOCATORS_DICT
from destination_codes import AIRPORT_CODES, DESTINATIONS

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    level=logging.INFO,
    filename="flight_scraper_logs.txt",
)
logger = logging.getLogger(__name__)

class FlightScraper:

    def __init__(self, city) -> None:
        user_agent = self.__generate_user_agent()
        options = Options()
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--no-sandbox")
        options.headless = True
        options.add_argument(f"user-agent={user_agent}")
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride", {"userAgent": f"{user_agent}"}
        )
        self.driver.get(
            "https://www.cheapflights.co.uk/flight-search/LHR-LAS/2021-12-20/2021-12-27?sort=bestflight_a"
        )
        self.__bypass_cookies()
        self.city = city
        self.airport_code = AIRPORT_CODES[self.city]
        logger.info(f"Initializing Scraper for {self.city}")
        
    @staticmethod
    def __generate_user_agent():
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [
            OperatingSystem.WINDOWS.value,
            OperatingSystem.LINUX.value,
            OperatingSystem.MAC_OS_X.value,
        ]
        user_agent_rotator = UserAgent(
            software_names=software_names,
            operating_systems=operating_systems,
            limit=100,
        )
        user_agent = user_agent_rotator.get_random_user_agent()
        return user_agent

    def __bypass_cookies(self) -> None:
        try:
            sleep(3)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, LOCATORS_DICT['COOKIES_POPUP']))
            )
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, LOCATORS_DICT['COOKIES_POPUP']))
            )
        except Exception as e:
            logger.error(f"{e}")
        finally:
            cookie = self.driver.find_element(By.XPATH, LOCATORS_DICT['COOKIES_POPUP'])
            cookie.click()

    def change_url(self, depart_date: str, return_date: str) -> None:
        curr_url = self.driver.current_url
        url_sections = curr_url.split("/")
        url_sections[-2] = depart_date
        logger.info(f"Depart date changed to {depart_date}")
        airport = url_sections[-3].split("-")
        airport[1] = self.airport_code
        url_sections[-3] = "-".join(airport)
        logger.info(f"Destination changed to {self.airport_code}")
        return_section = url_sections[-1].split("?")
        return_section[0] = return_date
        logger.info(f"Return date changed to {return_date}")
        url_sections[-1] = "?".join(return_section)
        new_url = "/".join(url_sections)
        sleep(0.05)
        self.driver.get(new_url)
        

    def get_flight_info(self, info) -> dict[str, str]:
        flight = {}
        sleep(2)
        depart_times = info.find_elements(By.XPATH, LOCATORS_DICT['DEPART_TIMES'])
        arrival_times = info.find_elements(By.XPATH, LOCATORS_DICT['ARRIVAL_TIMES'])
        num_stops = info.find_elements(By.XPATH, LOCATORS_DICT['NUM_STOPS'])
        flight_times = info.find_elements(By.XPATH, LOCATORS_DICT['FLIGHT_TIMES'])
        price = info.find_element(By.XPATH, LOCATORS_DICT['PRICE']).text
        airports = info.find_elements(By.XPATH, LOCATORS_DICT['AIRPORTS'])
        airline = info.find_element(By.XPATH, LOCATORS_DICT['AIRLINE'])
        
        if len(num_stops) == 2:
            origin_stops = num_stops[0].text
            return_stops = num_stops[1].text
        else:
            origin_stops = return_stops = num_stops[0].text
        
        if num_stops[0].text != 'direct':
            layover = info.find_element(By.XPATH, LOCATORS_DICT['LAYOVER']).text
        else:
            layover = 'N/A'
           
        
        flight["Origin-Flight"] = depart_times[0].text + " - " + arrival_times[0].text
        flight["Origin-Airport"] = airports[0].text.split('\n')[0]
        flight["Origin-Layover"] = layover
        flight["Origin-Airline"] = airline.text
        flight["Origin-Destination-Airport"] = airports[0].text.split('\n')[2]
        flight["Origin-Flight-Type"] = origin_stops
        flight["Origin-Flight-Duration"] = flight_times[0].text
        flight["Return-Flight"] = depart_times[1].text + " - " + arrival_times[1].text
        flight["Return-Airport"] = airports[1].text.split('\n')[0]
        flight["Return-Layover"] = layover
        flight["Return-Airline"] = airline.text
        flight["Return-Destination-Airport"] = airports[1].text.split('\n')[2]
        flight["Return-Flight-Type"] = return_stops
        flight["Return-Flight-Duration"] = flight_times[1].text
        flight["Price"] = price

        return flight

    def get_flight_info_driver(self) -> pd.DataFrame:
        try:
            sleep(2)
            logging.info(f"Getting information on flights for {self.city}")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, LOCATORS_DICT['FLIGHTS_CARD']))
            )
        except TimeoutException:
            logger.info(f"No flights available for {self.city}")
            pass
        else:
            sleep(3)
            flights_info = self.driver.find_elements(By.XPATH, LOCATORS_DICT['FLIGHTS_CARD'])
            list_of_flight_dicts = []
            for info in tqdm(
                flights_info, desc=f"Flight info progress for {self.city}", total=len(flights_info)
            ):
                flight = self.get_flight_info(info)
                flights_df = pd.DataFrame([flight], columns=flight.keys())
                list_of_flight_dicts.append(flights_df)
            flights_df = pd.concat(list_of_flight_dicts)
            flights_df.to_csv(
                f"{os.getcwd()}/flights_information/{self.city}_flights.csv", index=False
            )

    def scrape(self, depart_date: str, return_date: str) -> None:
        self.change_url(depart_date, return_date)
        self.get_flight_info_driver()
        self.driver.quit()


def _run_scrape(city: str) -> None:
    scraper = FlightScraper(city)
    scraper.scrape("2022-01-10", "2022-01-14")

_run_scrape("Faro")

class ThreadPoolExecutorWithQueueSizeLimit(ThreadPoolExecutor):
    def __init__(self, maxsize=5, *args, **kwargs):
        super(ThreadPoolExecutorWithQueueSizeLimit, self).__init__(*args, **kwargs)
        self._work_queue = queue.Queue(maxsize=maxsize)
def run():
    try:
        futures = set()
        with ThreadPoolExecutorWithQueueSizeLimit(max_workers=5) as executor:
            futures = [
                executor.submit(_run_scrape, city)
                for city in DESTINATIONS
                if Path(f"{os.getcwd()}/flights_information/{city}_flights.csv").exists()
                == False
            ]
        for scraper in futures:
            scraper.result()
    except StaleElementReferenceException:
        sleep(5)
        run()


run()

# %%
