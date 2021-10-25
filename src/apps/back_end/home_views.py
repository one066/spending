import datetime
import uuid

from flask import Blueprint, jsonify

from apps.back_end.models import RecordSpending, User
from apps.back_end.validator import AddSpendingValidator, LoginValidator
from extension.flask import class_route
from extension.flask.api import login_check, ok_response, v1
from extension.flask.base_views import BaseView
from extension.mysql_client import db
from extension.redis_client import redis_client
from SDK.email import OneEmail

home_view = Blueprint('home_view', __name__, url_prefix='/v1/service')


@class_route(home_view, '/add_spending')
class AddSpending(BaseView):
    validator = AddSpendingValidator

    def post(self, *args, **kwargs):
        login_check()

        request_data = self.get_request_data(kwargs)
        spending_id = uuid.uuid4().hex
        start_time = datetime.datetime.now().isoformat()

        _record_spending = RecordSpending(
            id=spending_id,
            start_time=start_time,
            title=request_data['title'],
            price=request_data['price'],
            people=self.get_name(),
        )

        db.session.add(_record_spending)
        db.session.commit()

        # 像成员发送消息
        OneEmail().send_pending(
            users=User.emails(),
            record_spending=_record_spending.show()
        )
        return ok_response('add success')


@class_route(home_view, '/show_spending')
class ShowSpending(BaseView):
    def get(self, *args, **kwargs):
        login_check()

        _record_spending = RecordSpending.query.all()
        return jsonify(
            {'data': [record.show() for record in _record_spending]})


@class_route(home_view, '/login_check')
class LoginCheck(BaseView):
    validator = LoginValidator

    def post(self, *args, **kwargs):
        request_data = self.get_request_data(kwargs)
        name = request_data['name']
        password = request_data['password']

        user = User.query.filter_by(name=name).first()
        if user.login(password):

            token = uuid.uuid4().hex
            redis_client.set(name, token)

            # 保留一个星期
            redis_client.expire(name, 60 * 60 * 24 * 7)

            return jsonify({
                'login': True,
                'token': token,
                'name': name,
            })
        return jsonify({'login': False})


@class_route(home_view, '/home_echarts_data')
class HomeEchartsData(BaseView):

    def get(self, *args, **kwargs):
        user = RecordSpending.get_home_echarts_data()
        return jsonify([{'value': value, 'name': key} for key, value in user.items()])
