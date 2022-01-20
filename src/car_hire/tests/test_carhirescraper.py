# %%
import unittest
import pandas as pd
import sys
sys.path.append('../')
from car_hire_scraper.CarScraper import CarHireScraper
from car_hire_scraper.locators import *
from pandas._testing import assert_frame_equal
from selenium import webdriver

class CarHireScraperTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.city = 'London'
        self.test = CarHireScraper()
        try:
            self.data = pd.read_csv('./London_carhire.csv',
            sep = ',',
            header = 0)
        except IOError:
            print('Can not open file')
    
    def test_scrape(self):
        df1 = self.test.scrape('London', '2022-02-10', '2022-02-14', False)
        df2 = self.data
        assert_frame_equal(df1 , df2)

   
    def tearDown(self) -> None:
        self.test.driver.quit()


unittest.main(argv=[''], verbosity=3, exit=False)

# %%