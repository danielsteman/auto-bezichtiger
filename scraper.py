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

def extract(driver, *, identifier, url):
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

driver = driver_init()

url = "https://www.pararius.nl/huurwoningen/amsterdam/wijk-bos-en-lommer,centrum-oost,centrum-west,de-baarsjes,de-pijp,indische-buurt,oostelijk-havengebied,oud-oost,oud-west,oud-zuid,rivierenbuurt,westelijk-havengebied,westerpark,zeeburgereiland,zuidas/1300-1750/3-aantalkamers/50m2"
lookup_class = "listing-search-item.listing-search-item--list.listing-search-item--for-rent"

data = extract(driver, identifier=lookup_class, url=url)
parsed_data = [listing.split('\n') for listing in data]
collection = [transform(line) for line in parsed_data]

loader = Loader()
loader.load(collection)

driver.close()
