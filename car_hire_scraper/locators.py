url = "https://www.cheapflights.co.uk/cars/"

cookie_button = '//button[@title="Accept"]'

all_destinations = '//div[@class="Common-Layout-Brands-Cheapflights-DynamicLinks popularMapDestinations"]'
destination_path = '//div[@class="Common-Layout-Brands-Cheapflights-DynamicLinks popularMapDestinations"]//ul/li/a/span[@class="linkText"]'

search_bar_path = '//div[@class="lNCO-inner"]'
search_bar_typing = '/html/body/div[5]/div/div[2]/div[1]/div[2]/div/input'
search_button = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[2]/button'
drop_down = '/html/body/div[5]/div/div[2]/div[2]/div/ul/li[2]/div/div[2]'

search = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[1]/div[1]/div/div'

car_card = './/div[@class="jo6g-Photo"]'
car_card_external = './/div[@class="jo6g-Photo jo6g-external"]'

car_type = './/div[@class="MseY-title js-title"]'
passengers = './/div[@aria-label="Passengers count"]'
location = './/div[@class="x9e3-address"]'

brands_section = './/div[@class="JwPH"]'
cheap_brand_section = './/div[@class="JwPH JwPH-mod-type-cheapest"]'

total_price = './/div[@class="JwPH-totalPrice JwPH-mod-variant-specialRate"]'
t_price = './/div[@class="JwPH-totalPrice"]'
pday = './/div[@class="JwPH-price"]'
supplier_x = './/img[@class="JwPH-logo"]'
rate = './/div[@class="mzui"]'

card = '//div[@class="jo6g"]'

car_xpath_dict = {
    'Car Type': car_type,
    'Number of Passengers' : passengers,
    'Location' : location
}

column_names = ['City', 'Car Type', 'Number of Passengers', 'Location']
car_dict = dict.fromkeys(column_names)

brand_dict = {
    'Supplier' : supplier_x,
    'Total Price' : total_price,
    'Price' : pday,
    'Offer Rating' : rate
}


pop_cities = ['Alicante',
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