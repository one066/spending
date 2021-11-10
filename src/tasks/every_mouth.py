import requests

from extension.project_config import get_config


def send_every_mouth_user_spending():
    """ 定时发邮箱
    """
    send_every_mouth_user_spending_url = get_config(
    ).SEND_EVERY_MOUTH_USER_SPENDING_URL
    response = requests.get(send_every_mouth_user_spending_url, verify=False)
    response.raise_for_status()
    print(response.json())
