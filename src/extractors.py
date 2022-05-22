class Extractor:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def extract(self):
        identifier = self.config.get('agents', 'pararius', 'class')
        url = self.config.get('agents', 'pararius', 'url')
        self.driver.get(url)
        result = self.driver.find_elements_by_class_name(identifier)
        if isinstance(result, list):
            return [e.text for e in result]
        return result.text