#-coding:utf-8--
from . import main
from flask import render_template


# test views
@main.route('/test/')
def test():
    return "<h1>just tell you everything is ok!</h1>"

@main.route('/toshare',methods = ['GET','POST'])
def toshare():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = Post(body = form.body.data,
					auther = current_user._get_current_object()
					share_type = form.post_type.data)      #分享OR原创
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('.index'))

@main.route('/feed/share',method = ['GET']
def post_share():
	form =PostForm()
	posts = Post.query.filter_by(post_type=form.post_type.data='share').order_by(Post.timestamp.desc()).all()
return render_template('share.html',form = form,posts = posts) #分享的文章页面

@main.route('/feed/original',method = ['GET']
def post_original():
	form = PostForm()
	posts = Post.query.filter_by(post_type=form.post_type.data ='original').order_by(Post.timestamp.desc()).all()
return render_template('original.html',form = form,posts = posts) #原创的文章页面
