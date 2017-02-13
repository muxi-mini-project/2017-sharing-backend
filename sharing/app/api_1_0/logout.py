#coding:utf-8
from . import api
from authentication import auth
from flask_login import login_required,logout_user
from flask import request,jsonify,Response


@api.route('/logout/')
@login_required
def logout():
    logout_user()
    return jsonify({
        "message":"您已登出"
        })