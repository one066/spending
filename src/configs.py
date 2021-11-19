from extension.base_config import BaseConfig


class Development(BaseConfig):
    STAGE = 'development'


class Production(BaseConfig):
    DEBUG = False
    STAGE = 'production'
