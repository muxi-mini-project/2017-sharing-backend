#coding:utf-8
from flask import url_for, flash, request,g, jsonify
from ..decorators import login_required   


#关注
@api.route("/follow/<int:id>", methods=['get', 'post'])
@login_required
def follow(id):
    if id not in user.followed.followed_id:
        user = User.query.filter_by(id=g.current_user.id).first()
        user.follow(User.query.filter_by(id=id).first())
        return jsonify({
            "message":'You have successfully followed the user'
          })
    else:
        return jsonify({
            "message":"You have already followed the user"
            })

#查看关注的人
@api.route("/followed_by/<int:id>", methods=['GET'])
@login_required
def followed_by(id):
    user = User.query.filter_by(id=id).first()
    followed = user.followed
    if followed:
        be_followed_users_id_list = [item.followed for item in followed]
        be_followed_users_id_list:
        username_list = [User.query.filter_by(id=user_id).first().username for user_id in be_followed_users_id_list]
    else:
        username = None
    return jsonify({'following_username':username_list})
#取消关注
@api.route("/unfollow/<int:id>")
@login_required
def unfollow(id):
    if id not inuser.followed.followed_id:
        user = User.query.filter_by(id=g.current_user.id).first()
        user.unfollow(User.query.filter_by(id=id).first())
        return jsonify({
            "message":"You have successfully unfollowed the user"
            })
    else :
        return jsonify({
            "message":"You haven't followed the user"
            })



