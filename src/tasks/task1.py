import requests


def task1():
    """ 定时发邮箱
    """
    response = requests.get(
        'http://127.0.0.1:5000/v1/service/send_every_mouth_user_spending')
    response.raise_for_status()
    print(response.json())
