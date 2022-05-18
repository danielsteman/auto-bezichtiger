import os
import logging
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from loader import Loader
from mapper import Mapper

load_dotenv()

if os.getenv("DEBUG") == "True":
    logging.basicConfig(level=logging.INFO)

def driver_init():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(
        ChromeDriverManager().install(),
        options=chrome_options
    )

def extract(driver, *, identifier: str, url: str):
    driver.get(url)
    result = driver.find_elements_by_class_name(identifier)
    if isinstance(result, list):
        return [e.text for e in result]
    return result

def transform(data):
    mapper = Mapper(data)
    if len(data) == 8:
        mapper._move_item_to_end(0)
    mapper.map()
    return mapper.mapped_data

estate_agents = {
    'vesteda': {
        'url': "https://www.vesteda.com/nl/woning-zoeken?s=Amsterdam,%20Nederland&sc=woning&priceFrom=1200&priceTo=2000&bedRooms=0&unitTypes=2&unitTypes=1&unitTypes=3&unitTypes=4&radius=20&placeType=1&lng=4.904139&lat=52.3675728&sortType=0",
        'lookup_class': "o-card o-card--listing o-card--shadow-small o-card--clickable",
    },
    'pararius': {
        'url': "https://www.pararius.nl/huurwoningen/amsterdam/wijk-bos-en-lommer,centrum-oost,centrum-west,de-baarsjes,de-pijp,indische-buurt,oostelijk-havengebied,oud-oost,oud-west,oud-zuid,rivierenbuurt,westelijk-havengebied,westerpark,zeeburgereiland,zuidas/1300-1750/3-aantalkamers/50m2",
        'lookup_class': "listing-search-item.listing-search-item--list.listing-search-item--for-rent",
    },
}

driver = driver_init()
data = extract(driver, identifier=estate_agents['pararius']['lookup_class'], url=estate_agents['pararius']['url'])
parsed_data = [listing.split('\n') for listing in data]
collection = [transform(line) for line in parsed_data]

loader = Loader()
loader.load(collection)

driver.close()
