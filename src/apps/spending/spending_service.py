import datetime
import uuid

from flask import Blueprint, jsonify

from apps.spending.models import RecordSpending, User
from apps.spending.validator import (AddSpendingValidator, LoginSerialize,
                                     LoginValidator)
from extension.flask import class_route
from extension.flask.api import failed_response
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

    def action(self, *args, **kwargs):
        spending_id = uuid.uuid4().hex
        start_time = datetime.datetime.now().isoformat()
        name = self.get_name()
        if not name:
            return failed_response('cookie', 'not name')
        _record_spending = RecordSpending(id=spending_id,
                                          start_time=start_time,
                                          title=self.validated_data['title'],
                                          price=self.validated_data['price'],
                                          people=self.get_name(),
                                          status='暂无')

        db.session.add(_record_spending)
        db.session.commit()

        # 向成员发送消息
        OneEmail().send_pending(users=User.emails(),
                                record_spending=_record_spending.show())
        return
