from flask import (Blueprint, redirect, render_template,
                   url_for)

from extension.flask import class_route
from extension.flask.base_views import BaseView

front_end_views = Blueprint('front_end_views',
                            __name__,
                            url_prefix='/spending',
                            template_folder='template',
                            static_url_path='',
                            static_folder='static')


@class_route(front_end_views, '/home')
class Home(BaseView):

    def get(self):
        return render_template('home.html')


@front_end_views.route('/', methods=['GET'])
def init():
    return redirect(url_for('front_end_views.Home'))


@front_end_views.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
