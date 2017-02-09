
#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required



from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,RadioField
from wtforms.validators import DataRequired,Required,Length,Email,Regexp,EqualTo

class PostForm(FlaskForm):
    body = TextAreaField("想分享点什么？", validators=[Required()])
    post_type = RadioField ('文章类型',choices = [('share','share' ),('original','original')])
    submit = SubmitField('发布')



class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


    
class EditProfileForm(Form):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'保存修改')

class EditProfileAdminForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1,64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(6, 64), ])
