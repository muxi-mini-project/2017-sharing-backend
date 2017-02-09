from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*arg, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*arg, **kwargs)
        return decorated_function
    return decoretor

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
