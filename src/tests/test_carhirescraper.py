# %%
import unittest
# unittest.defaultTestLoader.sortTestMethodsUsing = lambda *args: -1
import sys
sys.path.append('..')
from car_hire_scraper.CarScraper import CarHireScraper
import pandas as pd

class CarHireScraperTestCase(unittest.TestCase):

    @classmethod    
    def setUpClass(cls) -> None:
        pass
    
    def setUp(self) -> None:
        self.city = 'London'
        self.test = CarHireScraper()
        try:
            self.data = pd.read_csv('/home/faizmeghjee/AiCore Projects/cheapflights-webscraping-team/src/car_hire_scraper/Car_Hire_Data/London_carhire.csv',
            sep = ',',
            header = 0)
        except IOError:
            print('Can not open file')
    
    def test_1_cookie_click(self):
        self.assertTrue(self.test._cookie_click('//button[@title="Accept"]'))

    # def test_2_search_bar(self):
    #     # self.test._cookie_click('//button[@title="Accept"]')
    #     self.assertTrue(self.test._search_bar('//div[@class="lNCO-inner"]', self.city))

    # def test_3_date_period(self):
    #     self.test._cookie_click('//button[@title="Accept"]')
    #     self.test._search_bar('//div[@class="lNCO-inner"]', self.city)
    #     self.assertEqual('https://www.cheapflights.co.uk/cars/London,England,United-Kingdom-c28501/2022-01-10/2022-01-14;map?sort=rank_a', self.test._date_period('2022-01-10', '2022-01-14'))

    # def test_4_big_clicker(self):
    #     self.test._cookie_click('//button[@title="Accept"]')
    #     self.test._search_bar('//div[@class="lNCO-inner"]', self.city)
    #     self.test._date_period('2022-01-10', '2022-01-14')
    #     self.assertTrue(self.test._big_clicker())

    def test_5_scrape(self):
        pass
    
    # def test_5_car_card_main_info_scrape(self):
    #     self.test._cookie_click('//button[@title="Accept"]')
    #     self.test._search_bar('//div[@class="lNCO-inner"]', self.city)
    #     self.test._date_period('2022-01-10', '2022-01-14')
    #     self.test._big_clicker()
    #     self.assertIn('London', self.test._car_card_main_info_scrape('//div[@class="jo6g"]', self.city))
   
    def tearDown(self) -> None:
        self.test.driver.quit()


unittest.main(argv=[''], verbosity=3, exit=False)


# %%

# if __name__ == '__main__':
#     if __package__ is None:
#         import sys
#         from os import path
#         sys.path.append(path.dirname(path.dirname(path.abspath('locators.py'))))
#         from car_hire_scraper.locators import *
#     else:
#         from ..car_hire_scraper import locators
# %%
