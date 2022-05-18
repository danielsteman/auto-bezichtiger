class Extractor:
    def __init__(self):
        return self

    def _extract_digits(self, s: str):
        return int(''.join([i for i in s if i.isdigit()]))

    