from extension.base_config import BaseConfig


class Development(BaseConfig):
    STAGE = 'development'

    # local 激活定时任务的api
    SEND_EVERY_MOUTH_USER_SPENDING_URL = 'HTTP://127.0.0.1:5000/v1/service/send_every_mouth_user_spending'

    REDIS_HOST = '127.0.0.1'


class Production(BaseConfig):
    DEBUG = False
    STAGE = 'production'

    # 服务端 激活定时任务的api
    SEND_EVERY_MOUTH_USER_SPENDING_URL = 'https://121.43.135.49/v1/service/send_every_mouth_user_spending'
    REDIS_HOST = 'redis'

    # docker-compose mysql database url
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456hk@mysql:3306/spending?charset=utf8'