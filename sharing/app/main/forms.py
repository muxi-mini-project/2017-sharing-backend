#-coding:utf-8--

from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,RadioField

class PostForm(FlaskForm):
    body = TextAreaField("想分享点什么？", validators=[Required()])
	post_type = RadioField ('文章类型'，choices = [('share','share' )('original','original')])
    submit = SubmitField('发布')

