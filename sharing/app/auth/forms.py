#coding:utf-8
from flask_wtf import Form
from wtforms import StringField,PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Rexgexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField(u'账号', validators=[Required(), Length(1,64), 
                                                Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remeber_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class RegistrationForm(Form):
    email = StringField(u"账号", validators=[Required(), Length(1,64),
                                            Email()])
    username = StringField(u"昵称", validators=[
        Required(), Length(6,64), Rexgexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
            u'用户名必须以字母开头')])
    password = PasswordField(u'密码', validators=[
        Required(), Length(8,16),EquelTo('password2', message=u'密码必须匹配')])
    password2 = PasswordField(u'请再次输入密码', validators=[Required()])
    submit = Submit(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册')
