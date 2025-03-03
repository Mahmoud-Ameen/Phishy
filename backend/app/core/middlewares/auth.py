# libraries
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from functools import wraps

# app specific
from app.core.exceptions import AppException


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            raise AppException("Admin access required")
        return f(*args, **kwargs)
    return decorated_function
