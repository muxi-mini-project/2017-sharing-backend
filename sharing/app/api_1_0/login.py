#coding: utf-8
from  . import api 
from app import  db 
from flask import request,jsonify,Response
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User


@api.route('/login/',methods = ['GET','POST'])
def login():
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    try:
        user = User.query.filter_by(email = email).first()
    except:
        user = None
        user_id = None
    if user is not None and user.verify_password(password):
        login_user(user)
        user_id = current_user.id
        token = user.generate_confirmation_token()
        return jsonify({
            "user_id":user_id,
            "token":token
            })
