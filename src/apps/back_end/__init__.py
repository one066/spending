from apps.back_end.echarts_service import echarts_service
from apps.back_end.home_views import home_view

blueprints = [home_view, echarts_service]

__all__ = ['blueprints']
