#coding:utf-8
from flask import jsonify, redirect, request, url_for, flash
from ..models import User
from .. import db
from . import api

#注册
@api.route('/register/',methods = ['POST'])
def register():
        user = User.from_json(request.json)
        db.session.add(user)
        db.session.commit()
        #token = user.generate_confirmation_token()
        #send_email(user.email,'请确认你的账户',
        #                       'auth/email/confirm',user = user,token = token)
        #flash(u'确认邮件已经发往了你的邮箱')
        return jsonify(user.to_json()),201,\
        {
        'Location':url_for('api.get_user_id',id = user.id,_external = True)
        }       



