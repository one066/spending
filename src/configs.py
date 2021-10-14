import os
from datetime import timedelta


class initConfig(object):
    # INIT
    SECRET_KEY = os.urandom(24)
    # DEBUG = True
    # SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)   # 强制取消缓存
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=70)
    KEY = "x9uo3L1xDDcF58Pt"


class dbConfig(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456hk@127.0.0.1:3306/spending?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_RECYCLE = 800


class emailConfig(object):
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_DEBUG = True
    MAIL_USERNAME = '2531210067@qq.com'
    MAIL_PASSWORD = 'hivzkwegzwytecja'
