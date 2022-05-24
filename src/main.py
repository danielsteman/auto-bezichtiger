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
    batch_size = config.get('batch_size')

    dbutils.create_tables()

    while True:
        with Scraper(
            config=config,
            estate_agent='pararius',
            extractor=Extractor,
            transformer=ParariusTransformer,
            mapper=Mapper,
            loader=Loader,
            messenger=Messenger
        ) as scraper:
            for _ in range(batch_size):  # reinit the driver every `batch_size` times to free up memory
                try:
                    scraper.etl()
                    sleep(interval)
                except Exception as e:
                    logging.warning(f'Something went wrong.\n{e}')

