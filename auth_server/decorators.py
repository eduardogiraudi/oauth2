from functools import wraps
from flask import request
import responses

def require_params(param_names):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            json_data = request.get_json()
            missing_params = [param for param in param_names if param not in json_data]

            if missing_params:
                return responses.bad_request(
                    err='invalid request',
                    descr=f"Missing required parameters: {', '.join(missing_params)}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_args(arg_names):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            missing_args = [arg for arg in arg_names if arg not in request.args]

            if missing_args:
                return responses.bad_request(
                    err='invalid request',
                    descr=f"Missing required arguments: {', '.join(missing_args)}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
