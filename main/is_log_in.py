from flask import jsonify, session
from functools import wraps


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('logged_in') is True:
            return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized, Please Login"}), 401

    return wrap
