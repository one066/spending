import datetime
import uuid

from flask import Blueprint, jsonify

from apps.back_end.models import RecordSpending
from apps.back_end.validator import AddSpendingValidator, LoginValidator
from extension.flask import class_route
from extension.flask.base_views import BaseView, ok_response
from extension.mysql_client import db
from extension.redis_client import redis_client

home_view = Blueprint('home_view',
                 __name__,
                 url_prefix='/spending/v1/spending')


@class_route(home_view, '/add_spending')
class AddTodo(BaseView):
    validator = AddSpendingValidator

    def post(self, *args, **kwargs):
        request_data = self.get_request_data(kwargs)
        spending_id = uuid.uuid4().hex
        start_time = datetime.datetime.now().isoformat()

        _record_spending = RecordSpending(
            id=spending_id,
            start_time=start_time,
            title=request_data['title'],
            money=request_data['money'],
            people=request_data['people'],
        )
        db.session.add(_record_spending)
        db.session.commit()
        return ok_response('add success')


@class_route(home_view, '/show_todo')
class ShowTodo(BaseView):

    def get(self, *args, **kwargs):
        _record_spending = RecordSpending.query.all()
        return jsonify(_record_spending)


@class_route(home_view, '/login_check')
class LoginCheck(BaseView):

    validator = LoginValidator

    def post(self, *args, **kwargs):
        request_data = self.get_request_data(kwargs)
        password = request_data['password']
        name = request_data['name']

        if password == 'waitan405':
            token = uuid.uuid4().hex

            redis_client.set(name, token)
            redis_client.expire(name, 60 * 60 * 24)

            return jsonify({
                'login': True,
                'token': token,
            })
        return jsonify({'login': False})
