#coding:utf-8
#api路由函数用的装饰器
from functools import wraps
from flask import abort, request
from flask_login import current_user
from .models import Permission
import base64

def permission_required(permission):
    @wraps(f)
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*arfs, **kwargs)
        return decorated_function
    return decorator



def admin_required(f):
    '''
    认证管理员的装饰器
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token_header = request.headers.get('Authorization', None)
        if token_header:
            token_hash = token_header[6:]
            decode_token = base64.b64decode(token_hash)
            token = decode_token[:-1]
            g.current_user = User.verify_auth_token(token)
            if not g.current_user.is_administrator():
                return jsonify({'message':'Fobidden'}), 403
            return f(*args, **kwargs)
        else:
            return jsonify({'message':'401 unAuthorization'})
    return decorated

def login_required(f):
    '''
    要求登录的装饰器
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token_header = request.headers.get('Authorization', None)
        if token_header:
            token_hash = token_header[6:]
            decode_token = base64.b64decode(token_hash)
            token = decode_token[:-1]
            g.current_user.varify_auth_token(token)
            return f(*args, **kwargs)
        else:
            return jsonify({'message':'401 unAuthorization'}), 401
    return decorated

