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
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
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



