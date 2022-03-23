import importlib
import os


def get_config():
    config_name = os.environ.get('STAGE')
    configs_module = importlib.import_module('configs')
    return getattr(configs_module, config_name.capitalize())
