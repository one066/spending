import pandas as pd
from flask import Blueprint, jsonify

from apps.spending.models import RecordSpending, User
from apps.spending.validator import (LineDataSerialize, PieDataSerialize,
                                     PieValidator, ShowSpendingSerialize,
                                     StatusSerialize, StatusValidator,
                                     UsersSerialize)
from extension.flask import class_route
from extension.flask.views import GetView
from extension.mysql_client import db
from SDK.email import OneEmail, get_title

echarts_service = Blueprint('echarts_service',
                            __name__,
                            url_prefix='/v1/service')


@class_route(echarts_service, '/show_spending')
class ShowSpending(GetView):

    validated_class = PieValidator
    serialize_class = ShowSpendingSerialize

    def action(self, *arg, **kwargs):
        _record_spending = RecordSpending.query.filter_by(
            status=self.validated_data['status']).order_by(
                RecordSpending.start_time.desc()).all()
        return {'data': [record.show() for record in _record_spending]}


@class_route(echarts_service, '/pie_data')
class PieData(GetView):

    validated_class = StatusValidator
    serialize_class = PieDataSerialize

    def action(self, *arg, **kwargs):

        return {
            'data': RecordSpending.get_pie_dates(self.validated_data['status'])
        }


@class_route(echarts_service, '/get_names')
class GetNames(GetView):

    serialize_class = UsersSerialize

    def action(self):
        return {'names': RecordSpending.get_users()}


@class_route(echarts_service, '/get_status')
class GetStatus(GetView):

    serialize_class = StatusSerialize

    def action(self):
        status = RecordSpending.get_status()
        if '暂无' in status:
            status.remove('暂无')
        return {'status': status}


@class_route(echarts_service, '/line_data')
class LineData(GetView):

    validated_class = StatusValidator
    serialize_class = LineDataSerialize

    def action(self, *arg, **kwargs):
        dates = RecordSpending.get_dates()
        users = RecordSpending.get_users()
        series = RecordSpending.get_line_dates(self.validated_data['status'])

        return {
            'dates': dates,
            'users': users,
            'series': series,
        }


@class_route(echarts_service, '/send_every_mouth_user_spending')
class SendEveryMouthUserSpending(GetView):
    def action(self):
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
        return
