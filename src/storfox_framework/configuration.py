import os
import importlib

CONFIG_FILE = os.environ.get('CONFIG', 'config.development')


def config_vars():
    module = importlib.import_module(CONFIG_FILE)
    config_dict = {}

    for item in dir(module):
        if item.startswith('__'):
            continue

        if item.upper() != item:
            continue

        config_dict[item] = getattr(module, item)

    return config_dict


class Config(object):
    __instance = None
    __config = None

    def __new__(cls):
        if Config.__instance is None:
            Config.__instance = object.__new__(cls)

            cls.__config = importlib.import_module(CONFIG_FILE)

        return Config.__instance

    def __getattribute__(self, name):
        if name == 'config':
            return super().__getattribute__(name)
        return getattr(self.__config, name, None)


conf = Config()
