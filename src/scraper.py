import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from extractors import Extractor
from loader import Loader
from mapper import Mapper
from configurator import Config
from messenger import Messenger
from transformer import Transformer


class Scraper:
    def __init__(
        self,
        *,
        config: Config,
        estate_agent: str,
        extractor: Extractor,
        transformer: Transformer,
        mapper: Mapper,
        loader: Loader,
        messenger: Messenger,
        remote: str = None
    ):
        self.config = config
        self.estate_agent = estate_agent
        self.extractor = extractor
        self.transformer = transformer
        self.mapper = mapper
        self.loader = loader
        self.remote = remote
        self.messenger = messenger
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_argument("enable-automation")
        self.chrome_options.add_argument("--disable-browser-side-navigation")
    
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
        messenger = self.messenger()

        for row in data:
            result = loader.load(row)
            if result:
                msg=f"New listing found on {self.estate_agent}:\n{row.title}\n{row.address}\n{row.price}\n{row.sq_meters}\n{row.interior}\n\n{self.config.get('agents', self.estate_agent, 'url')}"
                messenger.send_notification(
                    msg=msg
                )
                logging.info(f"Message sent: {msg}")
                
        return data

    def __exit__(self):
        self.driver.close()