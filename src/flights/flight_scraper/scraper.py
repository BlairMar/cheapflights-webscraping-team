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
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
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
        logging.info("Initializing Scraper")
        user_agent = self.__generate_user_agent()
        options = Options()
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--no-sandbox")
        options.headless = True
        options.add_argument(f"user-agent={user_agent}")
        options.add_extension('../../Buster_Extension.crx')
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride", {"userAgent": f"{user_agent}"}
        )
        self.driver.get(
            "https://www.cheapflights.co.uk/flight-search/LHR-AMS/2021-12-02/2021-12-05?sort=bestflight_a"
        )
        self.__bypass_cookies()
        self.city = city
        self.airport_code = AIRPORT_CODES[self.city]
        
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
            sleep(0.05)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, LOCATORS_DICT['COOKIES_POPUP']))
            )
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, LOCATORS_DICT['COOKIES_POPUP']))
            )
        except Exception as e:
            if e == TimeoutException:
                os._exit()
            else:    
                logging.error(f"{e}", exc_info=True)
        finally:
            cookie = self.driver.find_element(By.XPATH, LOCATORS_DICT['COOKIES_POPUP'])
            cookie.click()

    def change_url(self, depart_date: str, return_date: str) -> None:
        curr_url = self.driver.current_url
        url_sections = curr_url.split("/")
        url_sections[-2] = depart_date
        logging.info(f"Depart date changed to {depart_date}")
        airports = url_sections[-3].split("-")
        airports[1] = self.airport_code
        url_sections[-3] = "-".join(airports)
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
        origin_container = info.find_elements(By.XPATH, LOCATORS_DICT['FLIGHTS_MAIN'])[0].text
        return_container = info.find_elements(By.XPATH, LOCATORS_DICT['FLIGHTS_MAIN'])[1].text
        airline = info.find_element(By.XPATH, LOCATORS_DICT['AIRLINE']).text
        flight["Origin-Flight"] = origin_container.split("\n")[0]
        flight["Origin-Airport"] = origin_container.split("\n")[1]
        flight["Airline"] = airline
        flight["Origin-Destination-Airport"] = origin_container.split("\n")[3]
        flight["Origin-Flight-Type"] = origin_container.split("\n")[4]
        flight["Origin-Flight-Duration"] = origin_container.split("\n")[5]
        flight["Return-Flight"] = return_container.split("\n")[0]
        flight["Return-Airport"] = return_container.split("\n")[1]
        flight["Return-Destination-Airport"] = return_container.split("\n")[3]
        flight["Return-Flight-Type"] = return_container.split("\n")[4]
        flight["Return-Flight-Duration"] = return_container.split("\n")[5]

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
                flights_info, desc="Flight info progress", total=len(flights_info)
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


# _run_scrape("Faro")
def run():
    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
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
