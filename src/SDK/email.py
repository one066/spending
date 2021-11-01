from flask_mail import Message

from extension.mail_client import mail


class OneEmail:
    def send_pending(self, users, record_spending):
        try:
            mail.connect()
            body = f'{record_spending[0]} 刚刚消费了\n {record_spending[1]} : {record_spending[2]}元'
            msg = Message("外滩405 开支",
                          sender='2531210067@qq.com',
                          recipients=users,
                          body=body,
                          charset='gbk')
            mail.send(msg)
            return True
        except:
            return False

    def every_mouth_data(self, users, title):
        try:
            mail.connect()
            body = f'本月开支表在附件里，分析情况请前去网页查看'
            msg = Message(f"外滩405 {title} 开支",
                          sender='2531210067@qq.com',
                          recipients=users,
                          body=body,
                          charset='gbk')

            with open('apps/front_end/static/data.xlsx') as fp:
                mail.attach("data.xlsx", 'application/octet-stream', fp.read())
            mail.send(msg)
            return True
        except:
            return False