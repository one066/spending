from typing import List

import pandas as pd
from flask import Blueprint
from sqlalchemy import func

from apps.spending.models import RecordSpending, User
from apps.spending.util import build_every_mouth_body, get_now_mouth_title
from apps.spending.validator import (LineDataSerialize, PieValidator,
                                     ShowSpendingSerialize,
                                     SpendingGroupByUserSerialize,
                                     StatusSerialize, StatusValidator)
from extension.flask import class_route
from extension.flask.views import GetView
from extension.mysql_client import db
from SDK.email import OneEmail

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


@class_route(echarts_service, '/spending_group_by_user')
class SpendingGroupByUser(GetView):
    validated_class = StatusValidator
    serialize_class = SpendingGroupByUserSerialize

    def action(self, *arg, **kwargs):
        group_spending = RecordSpending.get_spending_group_by_user(
            self.validated_data['status'])

        # 满足 echart.js 参数条件
        date = [{
            'name': spending.people,
            'value': '%.2f' % spending.value
        } for spending in group_spending]

        return {'data': date}


@class_route(echarts_service, '/status')
class Status(GetView):
    serialize_class = StatusSerialize

    NOW_STATUS = '暂无'

    def action(self):
        status = db.session.query(RecordSpending.status).group_by(
            RecordSpending.status).all()
        status = [_st.status for _st in status]

        # 排除当前月份的
        if self.NOW_STATUS in status:
            status.remove(self.NOW_STATUS)

        return {'status': status}


@class_route(echarts_service, '/line_data')
class LineData(GetView):
    validated_class = StatusValidator
    serialize_class = LineDataSerialize

    @staticmethod
    def _get_user_spending_by_status_and_date(user, status, date):
        return RecordSpending.query.filter(
            RecordSpending.status == status, RecordSpending.people == user,
            RecordSpending.start_time.like(f'{date}%')).order_by(
                RecordSpending.start_time.desc()).all()

    @staticmethod
    def _get_series_data(records) -> float:
        return sum([float('%.2f' % record.price)
                    for record in records]) if records else 0

    @staticmethod
    def _get_dates_by_status(status: str) -> List[str]:
        dates = db.session.query(
            func.date_format(
                RecordSpending.start_time,
                '%Y-%m-%d').label('date')).group_by('date').filter(
                    RecordSpending.status == status).order_by(
                        RecordSpending.start_time.asc()).all()
        return [date.start_time for date in dates]

    def action(self, *arg, **kwargs):
        status = self.validated_data['status']
        dates = self._get_dates_by_status(status)

        users = User.names()

        # 满足 echart.js 参数条件
        series = []
        for user in users:
            for date in dates:
                records = self._get_user_spending_by_status_and_date(
                    user, status, date)
                series_data = self._get_series_data(records)
                series.append({
                    'name': user,
                    'type': 'line',
                    'stack': 'Total',
                    'data': series_data
                })

        return {
            'dates': dates,
            'users': users,
            'series': series,
        }


@class_route(echarts_service, '/send_every_mouth_user_spending')
class SendEveryMouthUserSpending(GetView):
    SAVE_EXCEL_PATH = 'apps/front_end/static/data.xlsx'

    def _save_file(self):
        # TODO 没发现 api 暂时先保存下来、后面读取文件发送
        user_spending = db.session.query(
            RecordSpending.title, RecordSpending.people, RecordSpending.price,
            RecordSpending.start_time).filter_by(status='暂无').all()

        df = pd.DataFrame(user_spending,
                          columns=['title', 'name', 'price', 'start_time'])
        df.to_excel(self.SAVE_EXCEL_PATH, encoding='utf-8')

    def action(self):
        # 保存 excel
        self._save_file()

        # 发送邮件
        group_spending = RecordSpending.get_spending_group_by_user('暂无')
        now_mouth_title = get_now_mouth_title()
        every_mouth_body = build_every_mouth_body(group_spending)

        one_email = OneEmail()
        one_email.add_message(subject=f"外滩405 {now_mouth_title} 开支",
                              recipients=User.emails(),
                              body=every_mouth_body)
        one_email.add_attach(filename=f"外滩405 {now_mouth_title} 开支.xlsx",
                             content_type='application/octet-stream',
                             file_path=self.SAVE_EXCEL_PATH)
        one_email.send()

        # 更新数据库
        RecordSpending.query.filter(RecordSpending.status == '暂无').update(
            {'status': now_mouth_title})
        db.session.commit()
        return
