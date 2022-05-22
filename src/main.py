from dbutils import create_tables
from configurator import Config
from scraper import etl
from time import sleep

INTERVAL=30

if __name__ == "__main__":
    config = Config()
    create_tables()

    while True:
        etl('pararius', config=config)
        sleep(INTERVAL)
