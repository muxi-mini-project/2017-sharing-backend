#coding:utf-8
from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, Post
from ..email import send_email
from . import main
from .forms import NameForm,EditProfileAdminForm ,EditProfileForm, PostForm
from flask_login import current_user,login_required
from ..decorators import admin_required, permission_required

@main.route('/', methods=['GET', 'POST'])
def index():
    return "root directory"

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'您的个人页面已经修改成功')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/toshare',methods = ['GET','POST'])
def toshare():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
	post = Post(body = form.body.data,
		    auther = current_user._get_current_object(),  #获得当前对象
		    post_type = form.post_type.data)              #分享OR原创
	db.session.add(post)
	db.session.commit()
	return redirect(url_for('.index'))

#去分享的路由
@main.route('/feed/share',methods = ['GET'])
def post_share():
	posts = Post.query.filter_by(post_type = 'share').order_by(Post.timestamp.desc()).all()
	return render_template('share.html', posts = posts) #分享的文章页面

#博主原创的路由
@main.route('/feed/original',methods = ['GET'])
def post_original():
	form = PostForm()
	posts = Post.query.filter_by(post_type=form.post_type.data).filter_by(post_type = 'original').order_by(Post.timestamp.desc()).all()
	return render_template('original.html',form = form,posts = posts) #原创的文章页面

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)        #这个表需要一个user对象
    if form.validate_on_submit():
        user.email = form.email.data
        user.name = form.name.data
        user.location = form.location.data
        user.confirmed = form.comfirmed.data
        user.role = Role.query.get(form.role.data)#form.role.data返回的是一个int类型
        user.gender = form.gender.data            #也就是说这里返回一个int类型
        user.about_me = form.about_me.data
        db.session.add(user)
        flash(u'资料界面已被更新')
        return redirect(url_for('.user', username=user.name))
    form.email.data = user.email
    form.username.data = user.confirmed
    form.name.data = user.name
    form.location.data = user.location
    form.gender.data = user.gender                #我这里要返回一个string对象
    form.role.data = user.role_id                 #这个返回的是int值
    form.confirmed.data = user.confirmed
    form.about_me.data = user.abput_me
    return render_template('edit_profile.html', form=form, user=user)

#具体文章的路由
@main.route('/feed/post/<int:post_id>')
def show_post(post_id):
    render_template("share_post.html", post_id=id)

