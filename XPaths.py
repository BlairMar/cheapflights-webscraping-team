accept_cookies = '//*[@title="Accept"]'
cities_path = '//div[@class="Common-Layout-Brands-Cheapflights-DynamicLinks popularMapDestinations"]//ul/li/a/span[@class="linkText"]'
stays = '//a[@aria-label="Search for hotels"]'
hotels_searchbox = '//div[@role="textbox"]//div[@class="lNCO-inner"]'
search_button = '//button[@aria-label="Search"]'
exit_datebox = '//h2[@class="x92x-header x92x-pres-header-default"]'
hotel_name = '//h1[@class="c3xth-hotel-name"]'
address = '//div[@class="c3xth-address"]'
rating = '//span[@class="YlEV-rating-score"]'
reviewer_count = '//div[@class="YlEV-review-count"]'
cost = '//span[@class="c3xth-price"]'
provider = '//span[@class="c3xth-provider"]'
showmore = '//a[@class="moreButton"]'
hotel_results = '//div[@class="FLpo"]'

xpath_dict = {'Hotel Name': hotel_name,
              'Hotel Address' : address,
              'Average Rating' : rating,
              'Number of Reviews': reviewer_count,
              'Cost of Stay' : cost,
              'Provider' : provider}


column_names = ['City', 'Hotel Name', 'Hotel Address', 'Average Rating', 'Number of Reviews', 'Cost of Stay', 'Provider']
info_dict = dict.fromkeys(column_names)