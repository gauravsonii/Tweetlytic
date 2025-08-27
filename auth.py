from functools import wraps
from flask import request, jsonify


def require_bearer_token(token):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header:
                bearer, received_token = auth_header.split()
                if bearer.lower() == 'bearer' and received_token == token:
                    return f(*args, **kwargs)
            return jsonify({'error': 'Unauthorized'}), 401
        return decorated_function
    return decorator
