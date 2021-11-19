import os

from flask import Blueprint, jsonify, request

from extension.flask import class_route
from extension.flask.api import ok_response
from extension.flask.base_views import BaseView
from SDK.email import OneEmail

web_hook = Blueprint('web_hook', __name__, url_prefix='/v1/web_hooke')


@class_route(web_hook, '/accept')
class Accept(BaseView):
    def post(self, *args, **kwargs):
        name = request.json.get('name', 'no')

        if name in ['spending']:
            os.system(f'cd /usr/web/{name}/docker')
            os.system('docker-compose up')
            os.system('docker-compose down')

            OneEmail().send_success()
            return ok_response('success')

        return jsonify('failed')
