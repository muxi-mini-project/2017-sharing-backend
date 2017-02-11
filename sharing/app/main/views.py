#coding:utf-8
from flask import render_template, redirect, url_for, abort, flash, request,\
                  current_app, make_response
from .. import db
from ..models import Role, User, Post, Comment
from ..email import send_email
from . import main
from .forms import NameForm,EditProfileAdminForm ,EditProfileForm, PostForm,CommentForm
from flask_login import current_user,login_required
from ..decorators import admin_required, permission_required

@main.route('/', methods=['GET', 'POST'])
def index():
    return "root directory"
#用户资料页面
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

#去分享的路由
@main.route('/toshare',methods = ['GET','POST'])
def toshare():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
	post = Post(body = form.body.data,
		    auther = current_user._get_current_object(),  #获得当前对象
		    post_type = form.post_type.data)              #分享OR原创
	db.session.add(post)
	db.session.commit()
	return redirect(url_for('.post_share'))

#趣分享的路由
@main.route('/feed/share',methods = ['GET'])
def post_share():
        posts_queryobj = Post.query.filter_by(post_type ='share').order_by\
                (Post.timestamp.desc())
	page = request.args.get('page', 1, type=int)
        pagination = posts_queryobj.paginate(
                page, per_page=current_app.config['SHARING_POSTS_PER_PAGE'],
                error_out=False)
        posts = pagination.items
        return render_template('share.html', posts = posts) #分享的文章页面

#博主原创的路由
@main.route('/feed/original',methods = ['GET'])
def post_original():
	posts_queryobj = Post.query.filter_by(post_type =\
                'original').order_by(Post.timestamp.desc())
	page = request.args.get('page', 1, type=int)
        pagination = posts_queryobj.paginate(
                page, per_page=current_app.config['SHARING_POSTS_PER_PAGE'],
                error_out=False)
        posts = pagination.items
        return render_template('original.html',posts = posts) #原创的文章页面

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
@main.route('/feed/post/<int:post_id>', methods = ['GET','POST'])
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).get_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body = form.body.data,
                            post = post,
                            author = current_user._get_current_object())
        db.session.add(comment)
        flash('您的评论已提交')
        return redirect(url_for('.post',id = post_id,page = -1))
    page = request.args.get('page',1,type = int)
    if page == -1:
        page = (post.comments.count() - 1) / \
                current_app.config['FLASKY_COMMENTS_PRE_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
                    page,per_page = current_app.comfig['SHARING_COMMENTS_PRE_PAGE'],
                    error_out = False)
    comment = pagination.items
    return render_template("show_post.html", post=[post], form = form ,
                            comments = comments ,pagination = pagination)

#关注者的文章路由
@main.route('/feed/followed',methods = ['GET'])
def post_followed():
        query = current_user.followed_posts
        pagination = query.order_by(Post.timestamp.desc()).paginate(
                                    page,per_page =current_app.config['SHARING_POSTS_PER_PAGE'],
                                    error_out = False)
        posts = pagination.items
        return render_template('followed_post.html',posts=posts,pagination=pagination)

#show_post的编辑页面路由
@main.route('/edit_post/<int:post_id>', methods=['get', 'post'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit()
        post.body = form.body.data
        db.session.add(post)
        flash(u'这篇博文已经更新')
        return redirect(url_for('.show_post', post_id=post_id))
    form.body.data = post.body
    return render_template('edit_show_post.html', form=form)
