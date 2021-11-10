import pkgutil
from importlib import import_module

from flask import Flask
from flask_apscheduler import APScheduler

from extension.mail_client import mail
from extension.mysql_client import db
from extension.project_config import get_config


def create_app():
    config = get_config()
    app = Flask(__name__)
    app.config.from_object(config)

    # 定时任务
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    # 初始化组件
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
