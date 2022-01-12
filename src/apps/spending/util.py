from datetime import datetime
from typing import Dict, List

from dateutil.relativedelta import relativedelta

from apps.spending.models import RecordSpending


def get_now_mouth_title() -> str:
    """
    得这一个月的时间段
    `2021-12-12 to 2022-01-12`
    """
    last_time = datetime.strftime((datetime.now() - relativedelta(months=1)),
                                  '%Y-%m-%d')
    now_time = datetime.strftime(datetime.now(), '%Y-%m-%d')
    return f'{last_time} to {now_time}'


def build_every_mouth_body(record_spending: List[RecordSpending]) -> str:
    """
    构造每个人发送清单 body
    """
    # TODO 兼容手机和电脑 使用了 \n 和 <br> 换行
    body = '本月开支表在附件里，分析情况请前去网页查看 \n<br>'

    total_spending = sum(
        [float(spending.value) for spending in record_spending])
    body += f'总开支: {total_spending} \n<br>'

    average_spending = total_spending / len(record_spending)
    body += f'平均开支: {"%.2f" % average_spending} \n<br>'

    # 计算盈余
    for spending in record_spending:
        body += f'{spending.people} 开支: {spending.value}   '
        body += f'收入:{"%.2f" % (float(spending.people) - average_spending)} \n<br>'
    return body
