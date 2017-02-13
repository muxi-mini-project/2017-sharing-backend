#coding:utf-8
from flask import jsonify, redirect, request, url_for, flash,g
from ..models import Post
from .. import db
from . import api
from flask_login import login_required,current_user

from app.api_1_0.authentication import auth

#去分享的路由
@api.route('/toshare/',methods = ['POST'])
@login_required
def toshare():
    if request.method == 'POST':
        post = Post.from_json(request.json)
        post.author_id = current_user.id
        db.session.add(post)
        db.session.commit()
    return jsonify(post.to_json()), 201



