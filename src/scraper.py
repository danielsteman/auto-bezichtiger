import os
import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from extractors import Extractor
from loader import Loader
from mapper import Mapper
from configurator import Config
from transformer import Transformer

if os.getenv("DEBUG"):
    logging.basicConfig(level=logging.INFO)


class Scraper:
    def __init__(
        self,
        *,
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
        self.chrome_options.add_argument('--disable-dev-shm-usage')
    
    def __enter__(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
        if self.remote:
            self.driver.command_executor = self.remote
        return self

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