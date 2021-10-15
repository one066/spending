from functools import wraps

from flask import jsonify, redirect, request, url_for
from flask.views import MethodViewType

from extension.flask.exceptions import TokenFailed
from extension.redis_client import redis_client


def ok_response(result):
    new_body = {'ok': True, 'result': result}
    return jsonify(new_body)


def redirect_login():
    return jsonify({'redirect_login': True})


def failed_response(error_type, error_message):
    body = {
        'ok': False,
        'error_type': error_type,
        'error_message': error_message,
    }
    return jsonify(body)


def token_check(key, token):
    if not key:
        return False
    if key.decode() != token:
        return False

    return True


def v1(view):
    """
    view or func check
    """
    @wraps(view)
    def decorator(*args, **kwargs):
        cookie = request.cookies
        token = cookie.get('token', 'one')
        name = cookie.get('name', 'one')
        key = redis_client.get(name)

        if not token_check(key, token):
            if isinstance(view, MethodViewType):
                raise TokenFailed
            else:
                return redirect(url_for('front_end_views.login'))

        return view(*args, **kwargs)

    return decorator