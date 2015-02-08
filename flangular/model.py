# -*- coding: utf-8 -*-

from functools import wraps

from flask.ext.restful import abort, Resource

from . import core

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not core.user_valid(cookie=False):
            abort(401)
        return func(*args, **kwargs)
    return wrapper


class Resource(Resource):
    method_decorators = [authenticate]
