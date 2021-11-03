from flask_mail import Message

from extension.mail_client import mail


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

    def every_mouth_data(self, users, title):
        try:
            self.mail.connect()
            body = f'本月开支表在附件里，分析情况请前去网页查看'
            msg = Message(f"外滩405 {title} 开支",
                          sender='2531210067@qq.com',
                          recipients=users,
                          body=body,
                          charset='gbk')
            with open('apps/front_end/static/data.xlsx', 'rb') as fp:
                msg.attach(f'外滩405 {title} 开支.xlsx',
                           'application/octet-stream', fp.read())
            self.mail.send(msg)
            return True
        except Exception as ex:
            print(ex)
            return False
