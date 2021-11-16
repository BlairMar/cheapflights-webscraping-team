rom selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd

 

class CheapFlightsToursScraper:
    
    def __init__(self):
        self.driver_path = "C:\Program Files (x86)\chromedriver.exe"
        self.url = 'https://www.cheapflights.co.uk/things-to-do'
        self.service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=self.service)
        
    def load_page(self):
        self.driver.get(self.url)
        sleep(3)
        try:
            cookie_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(('xpath', '/html/body/div[2]/div/div[3]/div/div/div/div/div[1]/button[1]'))
            )
            
            cookie_btn.click()
        except NoSuchElementException:
            print('cookie button not found!')
    
    def search_city(self):
        search_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(('xpath', '//*[@id="root"]/div/div[2]/div/div/div[1]/form/div[1]'))
            )
        # sleep(5)
        # search_input = self.driver.find_element('xpath', '//*[@id="root"]/div/div[2]/div/div/div[1]/form/div[1]')
        search_input.click()

        search_input_focus = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(('xpath', '//input[@placeholder="Search for a city"]'))
            )
        search_input_focus.send_keys('London')
        sleep(3)
        search_input_focus.send_keys(Keys.ARROW_DOWN)

        first_city = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(('xpath', '/html/body/div[2]/div/div[2]/div[2]/div/ul/li[1]/div/div[2]'))).click()
        
        sleep(2)
        submit_btn = self.driver.find_element('xpath', '//button[@type="submit"]').click()
        sleep(15)

    def get_tours(self):
        search_tours = self.driver.find_element('xpath', '//*[@id="root"]/div/div[2]/div/div/div[4]/div[2]/div[1]/div[2]/a[1]')

        actions = ActionChains(self.driver)
        actions.move_to_element(search_tours)
        actions.perform()    
        search_tours.click()
        
        #search_tours.location_once_scrolled_into_view
        # self.driver.execute_script("arguments[0].scrollIntoView();", search_tours)
        # search_tours.click()

    def scroll_down(self):
        scroll_pause_time = 10
        i = 0

          # Get scroll height
        previous_height = self.driver.execute_script("return document.body.scrollHeight")

        while i < 5:
        # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
            sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
            current_height = self.driver.execute_script("return document.body.scrollHeight")
            if current_height == previous_height:
            # If heights are the same it will exit the function
                break
            
            previous_height = current_height
            i += 1

    # def create_csv_file(self):
    #     row_headers = ['Title', 'Rating', 'NumOfRatings', 'Price', 'Duration']
    #     csv_file = open('cheaptours.csv', 'w', encoding='utf-8', newline='')
    #     tours_csv = csv.DictWriter

        
    def scrape_data(self):

        soup = bs(self.driver.page_source, "lxml")
        tours = soup.find_all('div', class_="c0p_q")

        self.titles = []
        self.ratings = []
        self.number_of_ratings = []
        self.prices = []
        self.durations = []
        
        for tour in tours:
            title = tour.find('div', class_="c4Hod-title").text
            rating = tour.find('span', class_="nV2T-rating").text
            num_of_ratings = tour.find('span', class_="nV2T-rating-count-plain").text.lstrip('(').rstrip(')')
            price = tour.find('span', class_="c0p_q-price").text
            try:
                duration = tour.find('div', class_="sNnk-title").text
            except:
                duration = 'No data provided'
            
            self.titles.append(title)
            self.ratings.append(rating)
            self.number_of_ratings.append(num_of_ratings)
            self.prices.append(price)
            self.durations.append(duration)

    def save_to_df(self):
        df = pd.DataFrame({'titles' : self.titles,
        'ratings' : self.ratings,
        'number_of_ratings' : self.number_of_ratings,
        'prices' : self.prices,
        'durations' : self.durations
        })
        df.to_csv('cheaptours.csv', encoding='utf-8', index=False)



    

if __name__ == "__main__":
    scraper = CheapFlightsToursScraper()
    scraper.load_page()
    scraper.search_city()
    scraper.get_tours()
    scraper.scroll_down()
    scraper.scrape_data()
    scraper.save_to_df()
    scraper.driver.quit()