from functools import wraps

from flask import Blueprint, g, request
from flask.views import MethodViewType


def class_route(blueprint: Blueprint, rule, **options):
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
