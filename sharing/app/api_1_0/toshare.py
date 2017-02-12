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
        author = request.get_json().get("author")
        body = request.get_json().get("body")
        timestamp = request.get_json().get("timestamp")
        #post_type = request.get_json().get("post_type")
        post = Post(author = author,body = body,timestamp = timestamp)
        post_id = Post.query.first().id
        db.session.add(post)
        db.session.commit()
    return jsonify({
        "author":author,
        "body":body,
        "timestamp":timestamp,
        "post_id":post_id
        })