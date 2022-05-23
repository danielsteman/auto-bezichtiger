import logging
from configurator import Config
from extractors import Extractor
import dbutils
from loader import Loader
from mapper import Mapper
from scraper import Scraper
from time import sleep
from transformer import ParariusTransformer
from messenger import Messenger

if __name__ == "__main__":
    config = Config()
    interval = config.get('interval')
    messenger = Messenger()

    dbutils.create_tables()

    with Scraper(
        config=config,
        estate_agent='pararius',
        extractor=Extractor,
        transformer=ParariusTransformer,
        mapper = Mapper,
        loader = Loader
    ) as scraper:
        while True:
            try:
                scraper.etl()
                sleep(interval)
            except Exception as e:
                logging.warning(f'Something went wrong.\n{e}')
                messenger.send_notification(
                    msg='An error was raised during the house search.'
                )