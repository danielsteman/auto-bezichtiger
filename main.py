from dbutils import create_tables
from configurator import Config

if __name__ == "__main__":
    config = Config()
    config.read('settings.yaml')
    print(config.sections())
    print(config['app_name'])
    # create_tables()

