
#coding:utf-8
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,RadioField
from wtforms.validators import DataRequired,Required,Length,Email,Regexp,EqualTo
from flask.ext.pagedown import PageDownField

class PostForm(FlaskForm):
    body = PageDownField("想分享点什么？", validators=[Required()])
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
    username = StringField(u'用户名', validators=[Required()])
    confirmed = BooleanField(u'是否验证验证')
    role = SelectField(u'用户角色', coerce=int)
    gender = SelectField(u'性别')
    name = StringField(u'真实姓名')#长度有限制
    location = StringField(u'地址')#长度有限制
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'保存')
    

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.gender.choices = [u'男', u'女']
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被注册')

                


