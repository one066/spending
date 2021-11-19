from flask import request
from flask.views import MethodView

from extension.flask.api import failed_response


class BaseView(MethodView):
    validator = None

    def get_request_data(self, kwargs):
        request_data = self.parse_json()
        request_data.update(kwargs)
        deserializer = self.validator()
        request_data = deserializer.load(request_data)
        return request_data

    def get_request_data_v1(self, kwargs):
        request_data = {}
        for key, value in request.args.items():
            if isinstance(value, list) and len(value) == 1:
                request_data[key] = value[0]
            else:
                request_data[key] = value
        request_data.update(kwargs)
        deserializer = self.validator()
        request_data = deserializer.load(request_data)
        return request_data

    @classmethod
    def parse_json(cls):
        """解析 request body 为 json
        """
        return request.json or {}

    def dispatch_request(self, *args, **kwargs):
        try:
            return super(BaseView, self).dispatch_request(*args, **kwargs)
        except Exception as exception:

            # 自定义异常
            if hasattr(exception, 'error_type') and hasattr(
                    exception, 'error_message'):
                return failed_response(
                    error_type=exception.error_type,
                    error_message=exception.error_message,
                )
            # 系统异常
            else:
                print(exception)
                return failed_response(
                    error_type='bug',
                    error_message=repr(exception),
                )
