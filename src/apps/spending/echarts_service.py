import pandas as pd
from flask import Blueprint

from apps.spending.models.record_spending import RecordSpending as Rs
from apps.spending.models.user import User
from apps.spending.util import build_every_mouth_body, get_now_mouth_title
from apps.spending.validator import (LineDataSerialize, PieValidator,
                                     ShowSpendingSerialize,
                                     SpendingGroupByUserSerialize,
                                     StatusSerialize, StatusValidator)
from extension.flask import class_route
from extension.flask.views import GetView
from SDK.email import OneEmail

echarts_service = Blueprint('echarts_service',
                            __name__,
                            url_prefix='/v1/service')


@class_route(echarts_service, '/show_spending')
class ShowSpending(GetView):
    validated_class = PieValidator
    serialize_class = ShowSpendingSerialize

    def action(self, *arg, **kwargs):
        all_spending = Rs.get_time_desc_spending(self.validated_data['status'])
        # 通过 status 得到 所有开支，并时间降序
        return {'data': [spending.show() for spending in all_spending]}


@class_route(echarts_service, '/spending_group_by_user')
class SpendingGroupByUser(GetView):
    validated_class = StatusValidator
    serialize_class = SpendingGroupByUserSerialize

    def action(self, *arg, **kwargs):
        group_spending = Rs.get_spending_group_by_user(
            self.validated_data['status'])

        return {'data': group_spending}


@class_route(echarts_service, '/status')
class Status(GetView):
    serialize_class = StatusSerialize

    def action(self):
        status = Rs.get_status(remove_now_mouth=True)
        return {'status': status}


@class_route(echarts_service, '/user_spending_by_date')
class UserSpendingByDate(GetView):
    validated_class = StatusValidator
    serialize_class = LineDataSerialize

    def action(self, *arg, **kwargs):
        status = self.validated_data['status']
        dates = Rs.get_dates_by_status(status)

        users = User.names()

        user_spending = [
            Rs.get_user_spending_by_date(user, dates, status) for user in users
        ]

        return {
            'dates': dates,
            'users': users,
            'user_spending': user_spending,
        }


@class_route(echarts_service, '/send_every_mouth_user_spending')
class SendEveryMouthUserSpending(GetView):
    SAVE_EXCEL_PATH = 'apps/front_end/static/data.xlsx'

    def _save_file(self):
        user_spending = Rs.get_now_mouth_users_spending()

        # TODO 没发现 api 暂时先保存下来、后面读取文件发送
        df = pd.DataFrame(user_spending,
                          columns=['title', 'name', 'price', 'start_time'])
        df.to_excel(self.SAVE_EXCEL_PATH, encoding='utf-8')

    def _send_mail(self, now_mouth_title):
        group_spending = Rs.get_spending_group_by_user('暂无')
        every_mouth_body = build_every_mouth_body(group_spending)

        one_email = OneEmail()
        one_email.add_message(subject=f"外滩405 {now_mouth_title} 开支",
                              recipients=User.emails(),
                              body=every_mouth_body)
        one_email.add_attach(filename=f"外滩405 {now_mouth_title} 开支.xlsx",
                             content_type='application/octet-stream',
                             file_path=self.SAVE_EXCEL_PATH)
        one_email.send()

    def action(self):
        # 保存 excel
        self._save_file()

        now_mouth_title = get_now_mouth_title()

        # 发送邮件
        self._send_mail(now_mouth_title)
        # 更新数据库
        Rs.end_spending_for_the_mouth(now_mouth_title)
        return
