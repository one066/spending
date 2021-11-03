import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

from apps.back_end.models import RecordSpending, User
from extension.mysql_client import db
from SDK.email import OneEmail


def get_title():
    last_time = datetime.datetime.strftime(
        (datetime.datetime.now() - relativedelta(months=+1)), '%Y-%m-%d')
    now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    return f'{last_time}---{now_time}'


def task1():
    """ 定时发邮箱
    """
    df = pd.read_sql(
        '''select title, people, price, start_time from record_spending where status is null''',
        db.engine.raw_connection())
    df.to_excel('apps/front_end/static/data.xlsx', encoding='utf-8')
    title = get_title()

    # 发送邮件
    OneEmail().every_mouth_data(users=User.emails(), title=title)

    # 更新数据库
    RecordSpending.query.filter(RecordSpending.status == '暂无').update(
        {'status': title})
    db.session.commit()
