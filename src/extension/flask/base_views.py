from functools import wraps

from flask import jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError

from extension.flask.exceptions import TokenFailed
from extension.redis_client import redis_client
from small_broken_station_engine.model.password_crypto import PasswordCrypto
from small_broken_station_engine.model.password_save import PasswordSave


def ok_response(result):
    new_body = {'ok': True, 'result': result}
    return jsonify(new_body)


def redirect_login():
    new_body = {'login': True}
    return jsonify(new_body)


def failed_response(error_type, error_message):
    body = {
        'ok': False,
        'error_type': error_type,
        'error_message': error_message,
    }
    return jsonify(body)


def v1(view):
    @wraps(view)
    def decorator(*args, **kwargs):
        cookie = request.cookies
        token = cookie['token']
        user_id = cookie['user_id']
        time = cookie['time']

        key = redis_client.get(f'{user_id}:{token}')
        if not key:
            raise TokenFailed
        if key.decode() != time:
            raise TokenFailed

        return view(*args, **kwargs)

    return decorator


class BaseView(MethodView):
    validator = None

    def get_request_data(self, kwargs):
        request_data = self.parse_json()
        request_data.update(kwargs)
        deserializer = self.validator()
        request_data = deserializer.load(request_data)
        return request_data

    @staticmethod
    def encrypt(keys, text):
        key = PasswordSave().get_keys(keys)
        text = PasswordCrypto().rsa_encrypt(text, key[0])
        token = PasswordSave().random_key(
            50) + text + PasswordSave().random_key(50)
        return token

    @staticmethod
    def encrypt_v1(keys, text):
        key = PasswordSave().get_keys(keys)
        text = PasswordCrypto().rsa_encrypt(text, key[0])
        return text

    @classmethod
    def parse_json(cls):
        """解析 request body 为 json
        """
        return request.json or {}

    def dispatch_request(self, *args, **kwargs):
        try:
            return super(BaseView, self).dispatch_request(*args, **kwargs)
        except TokenFailed:
            return redirect_login()

        except Exception as exception:
            # 验证器
            if isinstance(exception, ValidationError):
                return failed_response(
                    error_type='validation_error',
                    error_message=exception.messages,
                )
            # 自定义异常
            elif hasattr(exception, 'error_type') and hasattr(
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
