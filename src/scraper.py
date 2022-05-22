import os
import logging
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from extractors import Extractor
from loader import Loader
from mapper import Mapper
from configurator import Config
from transformer import Transformer

load_dotenv()

if os.getenv("DEBUG") == "True":
    logging.basicConfig(level=logging.INFO)

def driver_init(remote_address: str = None):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    if remote_address:
        return webdriver.Chrome(
            command_executor=remote_address,
            options=chrome_options
        )
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
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

def etl(estate_agent: str, *, config: Config):
    identifier = config.get('agents', estate_agent, 'class')
    url = config.get('agents', estate_agent, 'url')
    driver = driver_init()
    data = extract(driver, identifier=identifier, url=url)
    parsed_data = [listing.split('\n') for listing in data]
    collection = [transform(line) for line in parsed_data]

    loader = Loader()
    loader.load(collection)

    driver.close()


class Scraper:
    def __init__(
        self,
        config: Config,
        estate_agent: str,
        extractor: Extractor,
        transformer: Transformer,
        mapper = Mapper,
        loader = Loader,
        remote: str = None
    ):
        self.config = config
        self.estate_agent = estate_agent
        self.extractor = extractor
        self.transformer = transformer
        self.mapper = mapper
        self.loader = loader
        self.remote = remote
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--no-sandbox')
    
    def __enter__(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
        if self.remote:
            self.driver.command_executor = self.remote

    def etl(self):
        extractor = self.extractor(self.driver, self.config)
        scraped_data = extractor.extract()
        transformer = self.transformer(scraped_data, self.mapper)
        data = transformer.transform()
        loader = self.loader()
        loader.load(data)
        return data

    def __exit__(self):
        self.driver.close()