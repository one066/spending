import datetime
import uuid

from flask import Blueprint

from apps.spending.models.record_spending import RecordSpending
from apps.spending.models.user import User
from apps.spending.validator import (AddSpendingValidator, LoginSerialize,
                                     LoginValidator)
from extension.flask import class_route
from extension.flask.api import view_check_token_v1
from extension.flask.views import PostView
from extension.mysql_client import db
from extension.redis_client import redis_client
from SDK.email import OneEmail

spending_service = Blueprint('spending_service',
                             __name__,
                             url_prefix='/v1/service')


@class_route(spending_service, '/login_check')
class LoginCheck(PostView):
    validated_class = LoginValidator
    serialize_class = LoginSerialize

    def action(self):
        name = self.validated_data['name']
        password = self.validated_data['password']
        user = User.query.filter_by(name=name).first()

        if user.login(password):
            token = redis_client.get(name)

            if token:
                token = token.decode()
            else:
                token = uuid.uuid4().hex
                redis_client.set(name, token)

            return {
                'login': True,
                'token': token,
                'name': name,
            }
        return {'login': False}


@class_route(spending_service, '/add_spending')
class AddSpending(PostView):
    validated_class = AddSpendingValidator

    @staticmethod
    def _send_mail(name: str, title: str, price: float) -> None:
        # 向成员发送消息
        one_email = OneEmail()
        one_email.add_message(subject="外滩405 开支",
                              recipients=User.emails(),
                              body=f'{name} 刚刚消费了\n {title} : {price}元')
        one_email.send()

    @view_check_token_v1
    def action(self, *args, **kwargs):
        name = self.get_name()
        title = self.validated_data['title']
        price = self.validated_data['price']

        # 添加开支
        _record_spending = RecordSpending(
            id=uuid.uuid4().hex,
            start_time=datetime.datetime.now().isoformat(),
            title=title,
            price=price,
            people=name,
            status='暂无')

        db.session.add(_record_spending)
        db.session.commit()

        self._send_mail(name, title, price)
        return
