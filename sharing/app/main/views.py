#coding:utf-8
from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm
from flask_login import current_user

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

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
					auther = current_user._get_current_object(),
					post_type = form.post_type.data)      #分享OR原创
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('.index'))

@main.route('/feed/share',method = ['GET'])
def post_share():
	form =PostForm()
	posts = Post.query.filter_by(post_type=form.post_type.data).filter_by(post_type = 'share').order_by(Post.timestamp.desc()).all()
	return render_template('share.html',form = form,posts = posts) #分享的文章页面

@main.route('/feed/original',method = ['GET'])
def post_original():
	form = PostForm()
	posts = Post.query.filter_by(post_type=form.post_type.data).filter_by(post_type = 'original').order_by(Post.timestamp.desc()).all()
	return render_template('original.html',form = form,posts = posts) #原创的文章页面

@admin
