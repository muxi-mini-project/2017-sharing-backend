#coding:utf-8
from flask_wtf import Form
from wtforms import StringField,PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField(u'账号', validators=[Required(), Length(1,64), 
                                                Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remeber_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

class RegisterForm(Form):
    email = StringField(u"账号", validators=[Required(), Length(1,64),
                                            Email()])
    username = StringField(u"昵称", validators=[
        Required(), Length(6,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
            u'用户名必须以字母开头')])
    password = PasswordField(u'密码', validators=[
        Required(), Length(8,16),EqualTo('password2', message=u'密码必须匹配')])
    password2 = PasswordField(u'请再次输入密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已被注册')
    
    def validate_username(self,filed):
	    if User.query.filter_by(username = filed.data).first():
		raise ValidationError(u'该用户名已被注册')


class ChangePasswordForm(FlaskForm):
	old_password = PasswordField(u'旧有密码',validators=[Required()])
	password = PasswordField(u'新密码',validators = [Required(),
							EqualTo('password2',message=u'密码须一致')])
	password2 = PasswordField(u'再次输入密码',validators = [Required()])
	submit = SubmitField(u'修改密码')

class ChangeUsername(FlaskForm):
    username = StringField('用户名',validators=[Required(), 
                                                Length(1, 64), 
                                                Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名须由字母，数字，点".",下划线"_"组成'
                                          )])
    submit = SubmitField(u'保存修改')


