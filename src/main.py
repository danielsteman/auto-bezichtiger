from dbutils import create_tables
from configurator import Config

if __name__ == "__main__":
    config = Config()
    print(config.get("agents"))
