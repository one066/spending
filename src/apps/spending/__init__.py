from apps.spending.echarts_service import echarts_service
from apps.spending.spending_service import spending_service

blueprints = [spending_service, echarts_service]

__all__ = ['blueprints']
