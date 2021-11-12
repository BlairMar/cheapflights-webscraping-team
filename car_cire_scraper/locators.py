url = "https://www.cheapflights.co.uk/cars/"
cookie_button = '//button[@title="Accept"]'
destination_path = '//ul/li/a/span[@class="linkText"]'
search_bar_path = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[1]/div[1]/div/div'
search_bar_typing = '/html/body/div[5]/div/div[2]/div[1]/div[2]/div/input'
search_button = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[2]/button'
search = '/html/body/div[1]/div[1]/main/div[1]/div[1]/div/div[1]/div/div/section/div[1]/div/div/div[2]/div[1]/div[1]/div/div'
drop_down = '/html/body/div[5]/div/div[2]/div[2]/div/ul/li[2]/div/div[2]'

view_deal_button = '//button[@class="Iqt3 Iqt3-mod-bold Button-No-Standard-Style Iqt3-mod-variant-solid Iqt3-mod-theme-progress-end Iqt3-mod-shape-rounded-small Iqt3-mod-shape-mod-left Iqt3-mod-spacing-small Iqt3-mod-size-small"]'
more_suppliers_button = '//div[@class="SB0e-More"]'

faux_click = '/html/body/div[1]/div/div[4]/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div[2]'
car_card = '//div[@class="jo6g-Photo"]'
car_card_external = '//div[@class="jo6g-Photo jo6g-external"]'

car_type = './/div[@class="MseY-title js-title"]'
passengers = './/div[@aria-label="Passengers count"]'
location = './/div[@class="x9e3-address"]'

brands_section = './/div[@class="c3YLU"]'

offer_rating = './html/body/div[1]/div/div[4]/div[2]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[1]/span/div/div[1]'
total_price = './/div[@class="JwPH-totalPrice JwPH-mod-variant-specialRate"]'
pday = './/div[@class="JwPH-price"]'
name = './/div[@class="SB0e-Name"]'
supplier_x = './/img[@class="JwPH-logo"]'
rate = './/div[@class="mzui"]'

card = '//div[@class="jo6g"]'

car_xpath_dict = {
    'Car Type': car_type,
    'Number of Passengers' : passengers,
    'Location' : location,
}

column_names = ['Car Type', 'Number of Passengers', 'Location', 'Brands']
car_dict = dict.fromkeys(column_names)

brand_dict = {
    'Supplier' : name,
    'Total Price' : total_price,
    'Price' : pday,
    'Rating' : rate,
    'Offer Rating' : offer_rating
}


# car_dict['brands'].append(brand_dict)