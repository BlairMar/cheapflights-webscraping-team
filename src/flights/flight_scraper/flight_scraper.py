#%%
import os
import logging
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from locators import LOCATORS_DICT
from destination_codes import AIRPORT_CODES, DESTINATIONS


class FlightScraper:
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        level=logging.INFO,
        filename="flight_scraper_logs.txt",
    )
    logging = logging.getLogger(__name__)

    def __init__(self, city) -> None:
        user_agent = self.__generate_user_agent()
        options = Options()
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--no-sandbox")
        # options.headless = True
        options.add_argument(f"user-agent={user_agent}")
        # options.add_extension('Buster_Extension.crx')
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
        logging.info(f"Initializing Scraper for {self.city}")
        
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
            logging.error(f"{e}")
        finally:
            cookie = self.driver.find_element(By.XPATH, LOCATORS_DICT['COOKIES_POPUP'])
            cookie.click()

    def change_url(self, depart_date: str, return_date: str) -> None:
        curr_url = self.driver.current_url
        url_sections = curr_url.split("/")
        url_sections[-2] = depart_date
        logging.info(f"Depart date changed to {depart_date}")
        airport = url_sections[-3].split("-")
        airport[1] = self.airport_code
        url_sections[-3] = "-".join(airport)
        logging.info(f"Destination changed to {self.airport_code}")
        return_section = url_sections[-1].split("?")
        return_section[0] = return_date
        logging.info(f"Return date changed to {return_date}")
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
        price = info.find_element(By.XPATH, LOCATORS_DICT['PRICE'])
        airports = info.find_element(By.XPATH, LOCATORS_DICT['AIRPORTS']).text
        
        if num_stops[0].text != 'direct':
            layover = info.find_element(By.XPATH, LOCATORS_DICT['LAYOVER']).text
        else:
            layover = 'N/A'        
        airline = info.find_elements(By.XPATH, LOCATORS_DICT['AIRLINE'])
        if len(airline) == 2:
            origin_airline = airline[0].text
            return_airline = airline[1].text
        else:
            origin_airline, return_airline = airline
            
        flight["Origin-Flight"] = depart_times[0].text + " - " + arrival_times[0].text
        flight["Origin-Airport"] = airports.split('-')[0]
        flight["Origin-Layover"] = layover
        flight["Origin-Airline"] = origin_airline
        flight["Origin-Destination-Airport"] = airports.split('-')[1]
        flight["Origin-Flight-Type"] = num_stops[0].text
        flight["Origin-Flight-Duration"] = flight_times[0].text
        flight["Return-Flight"] = depart_times[1].text + " - " + arrival_times[1].text
        flight["Return-Airport"] = airports.split('-')[1]
        flight["Return-Layover"] = layover
        flight["Return-Airline"] = return_airline
        flight["Return-Destination-Airport"] = airports.split('-')[0]
        flight["Return-Flight-Type"] = num_stops[1].text
        flight["Return-Flight-Duration"] = flight_times[1].text
        flight["Price"] = price

        return flight

    def get_flight_info_driver(self) -> pd.DataFrame:
        try:
            logging.info("Getting information on flights")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, LOCATORS_DICT['FLIGHTS_CARD']))
            )
        except TimeoutException:
            logging.info(f"No flights available for {self.city}")
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
# def run():
#     try:
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             futures = [
#                 executor.submit(_run_scrape, city)
#                 for city in DESTINATIONS
#                 if Path(f"{os.getcwd()}/flights_information/{city}_flights.csv").exists()
#                 == False
#             ]
#         for scraper in futures:
#             scraper.result()
#     except StaleElementReferenceException:
#         sleep(5)
#         run()


# run()

# %%
