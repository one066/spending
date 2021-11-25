import pandas as pd
from flask import Blueprint, jsonify

from apps.spending.models import RecordSpending, User
from apps.spending.validator import PieValidator, StatusValidator
from extension.flask import class_route
from extension.flask.base_views import BaseView
from extension.mysql_client import db
from SDK.email import OneEmail, get_title

echarts_service = Blueprint('echarts_service',
                            __name__,
                            url_prefix='/v1/service')


@class_route(echarts_service, '/show_spending')
class ShowSpending(BaseView):

    validator = PieValidator

    def get(self, *arg, **kwargs):
        request_data = self.get_request_data_v1(kwargs)
        _record_spending = RecordSpending.query.filter_by(
            status=request_data['status']).all()

        RecordSpending.query.filter(RecordSpending.status is None).update(
            {'status': '暂无'})
        return jsonify(
            {'data': [record.show() for record in _record_spending]})


@class_route(echarts_service, '/pie_data')
class PieData(BaseView):

    validator = StatusValidator

    def get(self, *arg, **kwargs):
        request_data = self.get_request_data_v1(kwargs)
        return jsonify(RecordSpending.get_pie_dates(request_data['status']))


@class_route(echarts_service, '/get_names')
class GetNames(BaseView):
    def get(self):
        return jsonify(RecordSpending.get_users())


@class_route(echarts_service, '/get_status')
class GetStatus(BaseView):
    def get(self):
        status = RecordSpending.get_status()
        status.remove('暂无')
        return jsonify(status)


@class_route(echarts_service, '/line_data')
class LineData(BaseView):
    validator = StatusValidator

    def get(self, *arg, **kwargs):
        request_data = self.get_request_data_v1(kwargs)
        dates = RecordSpending.get_dates()
        users = RecordSpending.get_users()
        series = RecordSpending.get_line_dates(request_data['status'])
        return jsonify({
            'dates': dates,
            'users': users,
            'series': series,
        })


@class_route(echarts_service, '/send_every_mouth_user_spending')
class SendEveryMouthUserSpending(BaseView):
    def get(self):
        user_data = db.session.query(
            RecordSpending.title, RecordSpending.people, RecordSpending.price,
            RecordSpending.start_time).filter_by(status='暂无').all()

        df = pd.DataFrame(user_data,
                          columns=['title', 'name', 'price', 'start_time'])
        df.to_excel('apps/front_end/static/data.xlsx', encoding='utf-8')

        # 发送邮件
        pie_dates = RecordSpending.get_pie_dates('暂无')
        OneEmail().every_mouth_data(users=User.emails(), pie_dates=pie_dates)

        # 更新数据库
        title = get_title()
        RecordSpending.query.filter(RecordSpending.status == '暂无').update(
            {'status': title})
        db.session.commit()
        return jsonify('ok')
