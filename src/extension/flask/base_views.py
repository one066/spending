from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from extension.flask.api import failed_response, redirect_login
from extension.flask.exceptions import TokenFailed


class BaseView(MethodView):
    validator = None

    def get_request_data(self, kwargs):
        request_data = self.parse_json()
        request_data.update(kwargs)
        deserializer = self.validator()
        request_data = deserializer.load(request_data)
        return request_data

    @classmethod
    def parse_json(cls):
        """解析 request body 为 json
        """
        return request.json or {}

    @classmethod
    def get_name(cls):
        cookie = request.cookies
        return cookie.get('name', 'x')

    def dispatch_request(self, *args, **kwargs):
        try:
            return super(BaseView, self).dispatch_request(*args, **kwargs)
        except TokenFailed:
            return redirect_login()

        # except Exception as exception:
        #     # 验证器
        #     if isinstance(exception, ValidationError):
        #         return failed_response(
        #             error_type='validation_error',
        #             error_message=exception.messages,
        #         )
        #     # 自定义异常
        #     elif hasattr(exception, 'error_type') and hasattr(
        #             exception, 'error_message'):
        #         return failed_response(
        #             error_type=exception.error_type,
        #             error_message=exception.error_message,
        #         )
        #     # 系统异常
        #     else:
        #         print(exception)
        #         return failed_response(
        #             error_type='bug',
        #             error_message=repr(exception),
        #         )
