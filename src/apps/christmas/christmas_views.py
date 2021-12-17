from flask import Blueprint, render_template, request

christmas_views = Blueprint('christmas_views',
                            __name__,
                            url_prefix='/',
                            template_folder='template',
                            static_url_path='',
                            static_folder='static')


@christmas_views.route('/christmas', methods=['GET'])
def christmas():
    name = request.args.get('name', '林嘚嘚')
    return render_template('index.html', name=name)
