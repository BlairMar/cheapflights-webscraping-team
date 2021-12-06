import unittest
from car_hire_scraper import CarHireScraper
from selenium.webdriver.firefox.options import Options 
from selenium import webdriver
import time
import os

class CarHireScraperTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.handle = open('CareHireScraper.py')
        self.city = 'London'
        self.test = CarHireScraper(self.city)
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.get("https://www.cheapflights.co.uk/cars/")

    def test_cookie_click(self):
        self.assertIsNone(self.test._cookie_click())

    def tearDown(self) -> None:
        self.test.driver.quit()


unittest.main(argv=[''], verbosity=3, exit=False)