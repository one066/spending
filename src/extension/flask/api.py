from functools import wraps

from flask import Blueprint, jsonify, redirect, request, url_for
from flask.views import MethodView, MethodViewType
from marshmallow import ValidationError

from extension.flask.exceptions import TokenFailed
from extension.redis_client import redis_client


def ok_response(result):
    body = {'ok': True, 'result': result}
    return jsonify(body)


def failed_response(error_type, error_message):
    body = {
        'ok': False,
        'error_type': error_type,
        'error_message': error_message,
    }
    return jsonify(body)


def class_route(blueprint: Blueprint, rule, **options):
    """class view 的路由
    """

    def decorator(view):
        if isinstance(view, MethodViewType):
            view_func = view.as_view(view.__name__)
        else:
            view_func = view

        blueprint.add_url_rule(
            rule, view.__name__, view_func=view_func, **options
        )
        return view

    return decorator


def handle_exception(view_name, exception, **kwargs):
    """处理异常
    APIException: 返回适当的错误信息
    else: 重新抛出异常
    """
    if isinstance(exception, ValidationError):
        return failed_response(
            error_type='ValidationError',
            error_message=exception.messages,
        )
    elif hasattr(exception,
                 'error_type') and hasattr(exception, 'error_message'):
        return failed_response(
            error_type=exception.error_type,
            error_message=exception.error_message,
        )
    else:
        raise exception


class APIBaseView(MethodView):
    """扩展 class based view, 增加异常处理
    """

    @property
    def user_id(self):
        return request.headers.get('x-authenticated-userid', None)

    @classmethod
    def parse_json(cls):
        """解析 request body 为 json
        """
        return request.json or {}

    @classmethod
    def get_name(cls) -> str:
        return request.cookies.get('name')

    def dispatch_request(self, *args, **kwargs):
        try:
            return super().dispatch_request(*args, **kwargs)
        except Exception as exception:
            return handle_exception(
                self.__class__.__name__, exception, **kwargs
            )


def token_check():
    cookie = request.cookies

    token = cookie.get('token')
    name = cookie.get('name')

    if not token or not name:
        return False

    key = redis_client.get(name)

    if not key:
        return False

    if key.decode() != token:
        return False

    return True


def view_check_token_v1(view):
    """
    view or func check
    """

    @wraps(view)
    def decorator(*args, **kwargs):
        if not token_check():
            raise TokenFailed
        return view(*args, **kwargs)

    return decorator


def func_check_token_v1(view):
    """
    view or func check
    """

    @wraps(view)
    def decorator(*args, **kwargs):
        if not token_check():
            return redirect(url_for('front_end_views.login'))
        return view(*args, **kwargs)

    return decorator
