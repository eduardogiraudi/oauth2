from functools import wraps
from flask import request, jsonify
import responses
def require_arg(arg_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if arg_name not in request.args:
                return responses.bad_request(err='invalid request',descr=f"Missing required arg: {arg_name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_param(param_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            json_data = request.get_json()
            if param_name not in json_data:
                return responses.bad_request(err='invalid request', descr=f"Missing required parameter: {param_name}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
