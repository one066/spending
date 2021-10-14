import datetime
import uuid

from flask import Blueprint, jsonify

from apps.back_end.models import RecordSpending
from apps.back_end.validator import AddSpendingValidator
from extension.flask import class_route
from extension.flask.base_views import BaseView, ok_response
from extension.mysql_client import db

home = Blueprint('home',
                 __name__,
                 url_prefix='/spending/v1/spending')


@class_route(home, '/add_spending')
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


@class_route(home, '/show_todo')
class ShowTodo(BaseView):

    def get(self, *args, **kwargs):
        _record_spending = RecordSpending.query.all()
        return jsonify(_record_spending)

