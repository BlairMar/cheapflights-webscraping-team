# %%
import unittest
from selenium.webdriver.firefox.options import Options 
import sys

sys.path.append('..')

from selenium import webdriver
import time
import os
from car_hire_scraper.CarScraper import CarHireScraper

# %%

class CarHireScraperTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.city = 'London'
        self.test = CarHireScraper()
    
    def test_cookie_click(self):
        self.assertTrue(self.test._cookie_click('//button[@title="Accept"]'))

    def test_date_period(self):
        self.assertEqual(self.test_date_period, 'https://www.cheapflights.co.uk/cars/London,England,United-Kingdom-c28501/2022-01-10/2022-01-14;map?sort=rank_a&fs=carfees=afterHoursFee')

    def tearDown(self) -> None:
        self.test.driver.quit()


unittest.main(argv=[''], verbosity=3, exit=False)
# %%