from flask import jsonify


def ok_response(result):
    new_body = {'ok': True, 'result': result}
    return jsonify(new_body)


def failed_response(error_type, error_message):
    body = {
        'ok': False,
        'error_type': error_type,
        'error_message': error_message,
    }
    return jsonify(body)
