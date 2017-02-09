<<<<<<< HEAD
#coding:utf-8
from flask import render_template, redirect, request, url_for, flash
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from flask_login import current_user 
=======
#-coding:utf-8--

from . import auth
from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from .forms import LoginForm,RegistrationForm,ChangePasswordForm
from flask.ext.login import current_user

@auth.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,'请确认你的账户',
                                'auth/email/confirm',user = user,token = token)

        flash('确认邮件已经发往了你的邮箱')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form = form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('auth.login'))
    if current_user.confirm(token):
        flash('你的账户已被确认,谢谢')
    else :
        flash('确认链接无效或过期')
    return redirect(url_for('auth.login'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'请确认你的账户',
                'auth/email/confirm',user = current_user,token = token)
    flash('新的确认邮件已经发往了你的邮箱')
    return redirect(url_for('main.index'))

@auth.route('/change-password',methods = ['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('你的密码已经被更改')
            return redirect(url_for('auth.login'))
        else:
            flash('密码无效')
    return render_template("auth/change_password.html,form = form ") #Without html documents


@auth.route('/change-username',method = ['GET','POST'])
@login_required
def change_username():
    form = ChangeUsername()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.add(current_user)
        flash('你的用户名已修改')
    return render_template("auth/change_username.html,form = form ")  #Without html documents
>>>>>>> ca681701843dee0fb437de0177d4a845bfcae024

@auth.route('/login', methods=['GET', 'POST'])
def login():
    ''' 登录系统 '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)
            flash(u"欢迎回来， %s ！" % current_user.username)
            #next键下保存了上一次用户登出的时url
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'您的邮箱地址或密码有误')
    return render_template('auth/login.html', form=form)

<<<<<<< HEAD
#登出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已经退出当前登录')
    return redirect(url_for('main.index'))

#注册功能待完成
@auth.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                  
                )

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        curretnt_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return render_template(url_for('auth.unconfirmed'))



=======

@auth.route('/logout')
@login_required

def logout():
    logout_user()
    flash('你的账号已登出。')
    return redirect(url_for('auth.login'))
>>>>>>> ca681701843dee0fb437de0177d4a845bfcae024

        
