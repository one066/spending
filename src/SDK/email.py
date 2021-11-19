from flask_mail import Message

from extension.mail_client import mail


class OneEmail:
    def __init__(self):
        self.mail = mail

    def send_success(self):
        try:
            self.mail.connect()
            body = '部署成功'
            msg = Message("服务器部署",
                          sender='2531210067@qq.com',
                          recipients=['1875874066@qq.com'],
                          body=body,
                          charset='gbk')
            self.mail.send(msg)
            return True

        except Exception as ex:
            print(ex)
            return False
