from flask import Blueprint
from flask.views import MethodViewType


def class_route(blueprint: Blueprint, rule, **options):
    """class view 的路由
    """
    def decorator(view):
        if isinstance(view, MethodViewType):
            view_func = view.as_view(view.__name__)
        else:
            view_func = view

        blueprint.add_url_rule(rule,
                               view.__name__,
                               view_func=view_func,
                               **options)
        return view

    return decorator
