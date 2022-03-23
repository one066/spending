import os

from extension.base_config import BaseConfig


class Development(BaseConfig):
    STAGE = 'development'

    # local 激活定时任务api
    SEND_EVERY_MOUTH_USER_SPENDING_URL = 'HTTP://127.0.0.1:5000/v1/service/send_every_mouth_user_spending'

    REDIS_HOST = 'redis'
    REDIS_PASSWORD = ''


class Production(BaseConfig):
    DEBUG = False
    STAGE = 'production'

    # 服务端 激活定时任务api
    SEND_EVERY_MOUTH_USER_SPENDING_URL = 'https://kkone.top/v1/service/send_every_mouth_user_spending'

    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

    # DATABASE URI

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}' \
                              f'@{os.environ.get("MYSQL_HOST")}:3306/spending?charset=utf8'
