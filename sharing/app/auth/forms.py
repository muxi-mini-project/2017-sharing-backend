#coding:utf-8
from flask_wtf import Form
from wtforms import StringField,PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email

class LoginForm(Form):
    email = StringField('邮箱地址', validators=[Required(), Length(1,64), 
                                                Email()])
    password = PasswordField('密码', validators=[Required()])
    remeber_me = BooleanField('记住我')
    submit = SubmitField('登录')
