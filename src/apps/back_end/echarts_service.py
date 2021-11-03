from flask import Blueprint, jsonify

from apps.back_end.models import RecordSpending
from apps.back_end.validator import PieValidator, StatusValidator
from extension.flask import class_route
from extension.flask.base_views import BaseView

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
