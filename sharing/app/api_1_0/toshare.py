#coding:utf-8
from flask import jsonify, redirect, request, url_for, flash
from ..models import Post,Permission
from .. import db
from . import api
from .decorators import permission_required
from app.api_1_0.authentication import auth

#去分享的路由
@api.route('/toshare/',methods = ['POST'])
@auth.login_required
def toshare():
    if request.method == 'POST':
        body = request.get_json().get("body")
        post_type = request.get_json().get("post_type")
        #author_id = Post.author_id
        post = Post(body = body,post_type=post_type)
        db.session.add(post)
        db.session.commit()
        author_id = post.query.first().author_id
        timestamp = post.query.first().timestamp
        post_id = post.query.first().id
    return jsonify({
        "body":body,
        "post_type":post_type,
        "author_id":author_id,
        "timestamp":timestamp,
        "post_id":post_id
        })