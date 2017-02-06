#coding:utf-8
from flask import render_template, redirect, request, url_for, flash
from . import auth
from ..models import User
from .forms import LoginForm
from flask_login import login_user


@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)
            return redirect(request.arg.get('next') or url_for('main.index'))
        flash('您的邮箱地址或密码有误')
    return render_template('auth/login.html', form=form)
