class Extractor:
    def __init__(self, driver, config, estate_agent):
        self.driver = driver
        self.config = config
        self.estate_agent = estate_agent

    def extract(self):
        identifier = self.config.get('agents', self.estate_agent, 'class')
        url = self.config.get('agents', self.estate_agent, 'url')
        self.driver.get(url)
        result = self.driver.find_elements_by_class_name(identifier)
        return [e.text for e in result]
