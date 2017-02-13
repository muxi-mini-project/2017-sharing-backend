#coding:utf-8
from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Post, Permission,Comment
from . import api
from .decorators import permission_required
from flask_login import login_required,current_user

#对应文章的评论
@api.route('/post/<int:id>/comments/')
def get_post_comment(id):
    post = Post.query.get_or_404(id)
    page = request.args.get('page',1,type = int)
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page,per_page = current_app.config['SHARING_COMMENT_PER_PAGE'],
        error_out = False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_post_comments', id=id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_post_comments', id=id, page=page+1, _external=True)
    return jsonify({
        'comments':[comment.to_json() for comment in comments],
        'prev':prev,      #prev变量储存了一个URL例如：/post/1/comments/
        'next':next,      #next变量储存了一个URL例如：/post/3/comments/
        'count':pagination.total
        })

#撰写评论
@api.route('/post/<int:id>/comments/',methods = ['POST'])
def new_post_comment(id):
  if request.method == 'POST':   
    post = Post.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author_id = current_user.id
    comment.post = post 
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()),201
