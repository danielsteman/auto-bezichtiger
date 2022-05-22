from functools import reduce
from typing import Union
import yaml
from yaml.loader import SafeLoader
import operator


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    def __init__(self):
        with open('settings.yaml') as f:
            self.config = yaml.load(f, Loader=SafeLoader)

    def get(self, *keys: tuple):
        return reduce(operator.getitem, keys, self.config)

    def set(self, *keys: tuple, value: Union[str, int]):
        self.get(list(keys)[:-1])[list(keys)[-1]] = value
