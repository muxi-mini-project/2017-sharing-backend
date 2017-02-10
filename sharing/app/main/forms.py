
#coding:utf-8
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import Required
from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,RadioField
from wtforms.validators import DataRequired,Required,Length,Email,Regexp,EqualTo
from flask_pagedown.fields import PageDownField

class PostForm(Form):
    #张可，看到的话提醒你一句，这里的FlaskForm和From是一个东西不要重复导入
    #知道啦
    body = PageDownField(u"想分享点什么？", validators=[Required()])
    post_type = RadioField (u'文章类型',choices =\
            [('share',u'趣分享'),('original', u'博主原创')])
    submit = SubmitField('发布')

class CommentForm(Form):
    body = StringField('',validators = [Required()])
    submit = SubmitField('评论')
    
class NameForm(Form):
    name = StringField(u'您的姓名', validators=[Required()])
    submit = SubmitField(u'提交')


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
    gender = SelectField(u'性别', coerce=int)
    name = StringField(u'真实姓名')#长度有限制
    location = StringField(u'地址')#长度有限制
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'保存')
    

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.gender.choices = [(1,u'男'),
                               (0,u'女')]#这样写下拉列表中会出现‘男’，‘女’两种选项吗？
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被注册')

                


