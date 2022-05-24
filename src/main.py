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
    retry_pause = config.get('retry_pause')
    retry_limit = config.get('retry_limit')
    messenger = Messenger()

    dbutils.create_tables()

    with Scraper(
        config=config,
        estate_agent='pararius',
        extractor=Extractor,
        transformer=ParariusTransformer,
        mapper=Mapper,
        loader=Loader,
        messenger=Messenger
    ) as scraper:
        while True:
            fails = 0
            try:
                scraper.etl()
                fails = 0
                sleep(interval)
            except Exception as e:
                logging.warning(f'Something went wrong.\n{e}')
                fails += 1
                sleep(retry_pause)
                if fails == retry_limit:
                    messenger.send_notification(
                        msg=f'An error was raised {fails} times during the house search.'
                    )
                    break