#coding:utf-8
from flask import redirect, request, url_for, flash
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm,ChangePasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from .. import db



@auth.route('/change-password',methods = ['GET','POST'])
@login_required
def change_password():
        if  current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash(u'你的密码已更改')
            return redirect(url_for('auth.login'))
        else:
            flash(u'密码无效')

        return jsonify(user.to_json()),201,\
        {
        url_for('api.get_user_id',id = user.id,_external = True)
        }
        