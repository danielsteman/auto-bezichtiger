from configurator import Config
from extractors import Extractor
from mapper import Mapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

config = Config()
driver = driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
estate_agent = "vesteda"

extractor = Extractor(driver=driver, config=config, estate_agent=estate_agent)

identifier = config.get('agents', estate_agent, 'class')
url = config.get('agents', estate_agent, 'url')

page = driver.get(url)
result = driver.find_elements_by_class_name(identifier)
parsed_data = [e.text for e in result]
exclude_values = ["slaap\xadkamer(s)", "Appartement", "per maand", "Oppervlakte", "BEKIJK WONING"]
data = [i.split('\n') for i in parsed_data]
data = [word for sentence in data for word in sentence if word not in exclude_values]
rows = list(zip(*(iter(data),) * 6))
for row in rows:
    ('3', '110 m²', 'Verhuurd onder voorbehoud', 'Spijkerboorweg 114', 'Haarlem', '€ 1295,-')
    mapped_row = ['Appartement', row[3], row[5], row[1], row[0], 'Interieur onbekend', 'Makelaar onbekend', row[2], 'self.estate_agent']
    mapper = Mapper(mapped_row)

    print(mapped_row)