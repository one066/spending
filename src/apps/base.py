import pkgutil
from importlib import import_module

from flask import Flask

from configs import dbConfig, emailConfig, initConfig
from extension.caching_client import cache
from extension.mail_client import mail
from extension.mysql_client import db


def create_app():
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(initConfig)
    app.config.from_object(emailConfig)
    app.config.from_object(dbConfig)

    # 初始化组件
    cache.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    # 加载 blueprint
    for module in pkgutil.iter_modules(['apps']):
        if module.ispkg is False:
            continue
        sub_app = import_module(f'apps.{module.name}')
        for blueprint in sub_app.blueprints:
            app.register_blueprint(blueprint)

    return app
