chrome_path = '/cheapflights-webscraping-team/chromedriver'

accept_cookies = '//*[@title="Accept"]'
cities_path = '//div[@class="Common-Layout-Brands-Cheapflights-DynamicLinks popularMapDestinations"]//ul/li/a/span[@class="linkText"]'
stays = '//a[@aria-label="Search for hotels"]'
hotels_searchbox = '//div[@role="textbox"]//div[@class="lNCO-inner"]'
hotel_box = '//div[@role="textbox"]'
hotels_box = '//div[@role="textbox"]'
search_button = '//button[@aria-label="Search"]'
exit_datebox = '//h2[@class="x92x-header x92x-pres-header-default"]'
hotel_name_xpath = '//h1[@class="c3xth-hotel-name"]'
address = '//div[@class="c3xth-address"]'
old_rating = '//span[@class="YlEV-rating-score"]'
rating = '//div[@class="l3xK-reviews-summary-score"]'
reviewer_count = '//div[@class="l3xK-reviews-summary-review-data"]'
reviewer_count_2 = '//div[@class="b40-rating-count"]'
old_reviewer_count = '//div[@class="YlEV-review-count"]'
cost = '//span[@class="c3xth-price"]'
provider = '//span[@class="c3xth-provider"]'
showmore = '//a[@class="moreButton"]'
hotel_results = '//div[@class="FLpo"]'

xpath_dict = {'Hotel Name': hotel_name_xpath,
              'Hotel Address' : address,
              'Average Rating' : rating,
              'Number of Reviews': reviewer_count,
              'Cost of Stay' : cost,
              'Provider' : provider}


column_names = ['City', 'Hotel Name', 'Hotel Address', 'Average Rating', 'Number of Reviews', 'Cost of Stay', 'Provider']
info_dict = dict.fromkeys(column_names)

cheap_flights_url = 'https://www.cheapflights.co.uk'
images_xpath = '//div[@class="f800-image-container"]'

cities = ['Alicante',
 'Amsterdam',
 'Bali',
 'Bangkok',
 'Barcelona',
 'Belfast',
 'Benidorm',
 'Berlin',
 'Budapest',
 'Dalaman',
 'Dubai',
 'Dublin',
 'Edinburgh',
 'Faro',
 'Florida',
 'Hong Kong',
 'Ibiza',
 'Lanzarote',
 'Las Vegas',
 'Lisbon',
 'London',
 'Los Angeles',
 'Malaga',
 'Malta',
 'Murcia',
 'New York',
 'Orlando',
 'Paris',
 'Prague',
 'Rome',
 'Tenerife',
 'Toronto']

 