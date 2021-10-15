import random

from flask_mail import Message

from extension.mail_client import mail


class OneEmail:
    def send_password(self, user_mail, password_key, password_value):
        try:
            mail.connect()
            code = str(random.randint(0, 999999)).rjust(6, '0')
            body = f'您的账号为:{password_key}\n您的密码为{password_value}\n请注意保管'
            msg = Message("one 小破站",
                          sender='2531210067@qq.com',
                          recipients=user_mail,
                          body=body,
                          charset='gbk')
            mail.send(msg)
            return code
        except:
            return False
