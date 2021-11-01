import datetime

from SDK.email import OneEmail
from apps.back_end.models import RecordSpending, User
from extension.mysql_client import db
import pandas as pd
from dateutil.relativedelta import relativedelta


def get_title():
    last_time = datetime.datetime.strftime((datetime.datetime.now() - relativedelta(months=+1)), '%Y-%m-%d')
    now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    return f'{last_time}到{now_time}'


def task1():
    """ 定时发邮箱
    """
    df = pd.read_sql(
        '''select title, people, price, start_time from record_spending where status is null''',
        db.engine.raw_connection()
    )
    df.to_excel('apps/front_end/static/data.xlsx')
    title = get_title()
    print(OneEmail().every_mouth_data(users=User.emails(),
                                      title=title))


if __name__ == '__main__':
    task1()
