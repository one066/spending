import datetime

from dateutil.relativedelta import relativedelta
from flask_mail import Message

from extension.mail_client import mail


def build_every_mouth_data_body(users_data):
    average = sum([float(user_data['value'])
                   for user_data in users_data]) / len(users_data)
    body = f'本月开支表在附件里，分析情况请前去网页查看<br>\n平均值:{average}<br>\n'
    for user_data in users_data:
        body += f'{user_data["name"]} 开支为{user_data["value"]}: ' \
                f'{user_data["value"]}-{average}={"%.2f" %(float(user_data["value"]) - average)}<br>\n'
    return body


def get_title():
    """得到当前时间段 title
    """
    last_time = datetime.datetime.strftime(
        (datetime.datetime.now() - relativedelta(months=+1)), '%Y-%m-%d')
    now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    return f'{last_time}---{now_time}'


class OneEmail:
    def __init__(self):
        self.mail = mail

    def send_pending(self, users, record_spending):
        try:
            self.mail.connect()
            body = f'{record_spending[0]} 刚刚消费了\n {record_spending[1]} : {record_spending[2]}元'
            msg = Message("外滩405 开支",
                          sender='2531210067@qq.com',
                          recipients=users,
                          body=body,
                          charset='gbk')
            self.mail.send(msg)
            return True

        except Exception as ex:
            print(ex)
            return False

    def every_mouth_data(self, users, pie_dates):
        title = get_title()
        try:
            self.mail.connect()
            body = build_every_mouth_data_body(pie_dates)
            msg = Message(f"外滩405 {title} 开支",
                          sender='2531210067@qq.com',
                          recipients=users,
                          body=body,
                          charset='gbk')

            with open('apps/front_end/static/data.xlsx', 'rb') as fp:
                msg.attach(filename=f'外滩405 {title} 开支.xlsx',
                           content_type='application/octet-stream',
                           data=fp.read())
            self.mail.send(msg)
            return True
        except Exception as ex:
            print(ex)
            return False
