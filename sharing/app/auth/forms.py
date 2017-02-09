<<<<<<< HEAD
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
=======
#-coding:utf-8--

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired,Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(Form):
	email = StringField('邮箱',validators=[Required(), Length(1, 64),
                                             Email()])
	username = StringField('用户名',validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名须由字母，数字，点“.",下划线”_“组成 '
                                          )])
	password = PasswordField('密码',validators = [
		Required(),EqualTo('password2',message = 'Password must match.')])
	password2 = PasswordField('确认密码',validators = [Required()])
	submit = SubmitField('注册')

	def validate_email(self,filed):
		if User.query.filter_by(email = filed.data).first():
			raise ValidationError('该邮箱已被注册.')

	def valodate_username(self,filed):
		if User.query.filter_by(username = filed.data).first():
			raise ValidationError('该用户名已被注册.')


class LoginForm(Form):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('旧有密码',validators=[Required()])
	password = PasswordField('新密码',validators = [Required(),
								EqualTo('password2',message = '密码须一致')])
	password2 = PasswordField('再次输入密码',validators = [Required()])
	submit = SubmitField('修改密码')

class ChangeUsername(FlaskForm):
	username = StringField('用户名',validators=[
    Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '用户名须由字母，数字，点“.",下划线”_“组成 '
                                          )])
	submit = SubmitField('修改用户名')

>>>>>>> ca681701843dee0fb437de0177d4a845bfcae024

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已被注册')
