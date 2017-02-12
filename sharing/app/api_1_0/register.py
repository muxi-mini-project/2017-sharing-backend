#coding:utf-8
from flask import jsonify, redirect, request, url_for, flash
from ..models import User
from .. import db
from . import api

#注册
@api.route('/register/',methods = ['POST'])
def register():
        if request.method == 'POST':
            email = request.get_json().get("email")
            password = request.get_json().get("password")
            username = request.get_json().get("username")
            user = User ( username= username,email=email ,password=password)
            db.session.add(user)
            db.session.commit()
            user_id=User.query.filter_by(email=email).first().id
        #token = user.generate_confirmation_token()
        #send_email(user.email,'请确认你的账户',
        #                      'auth/email/confirm',user = user,token = token)
        #flash(u'确认邮件已经发往了你的邮箱')
        return jsonify({
                "created":user_id
                })


