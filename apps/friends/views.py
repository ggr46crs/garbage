from apps.app import db
from sqlalchemy import or_,and_,not_,asc,desc
from apps.auth.forms import SignUpForm, LoginForm
from apps.auth.models import User
from apps.friends.models import Friends
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user,current_user
import requests
friends = Blueprint(
    "friends",
    __name__,
    template_folder = "templates",
    static_folder = "static",
)

@friends.route('/search')
@login_required
def search():
    friends_id = [row[0] for row in db.session.query(Friends.friend_id).filter(Friends.user_id == current_user.id).all()]
    
    # 並べ替え条件を取得
    sort_by = request.args.get('sort_by', 'username')  # デフォルトは 'username'
    order = request.args.get('order', 'asc')  # デフォルトは昇順

    # 有効な並べ替えカラムを指定
    valid_sort_columns = ["username", "email", "place1", "place2"]
    if sort_by not in valid_sort_columns:
        sort_by = "username"  # 無効な値が渡された場合は 'username' にフォールバック
    order_func = desc if order == "desc" else asc  # 降順なら desc、昇順なら asc を使用

    # 検索条件を取得
    text_input = request.args.get('search')
    if text_input is None or len(text_input) == 0:
        users = db.session.query(User).filter(
            and_(User.place1 == current_user.place1, User.id != current_user.id)
        ).order_by(order_func(getattr(User, sort_by))).all()
    else:
        users = db.session.query(User).filter(
            and_(
                User.place1 == current_user.place1,
                User.id != current_user.id,
                or_(
                    User.username.like(f"%{text_input}%"),
                    User.email.like(f"%{text_input}%")
                )
            )
        ).order_by(order_func(getattr(User, sort_by))).all()

    return render_template('friends/search.html', users=users, friends_id=friends_id, current_sort=sort_by, current_order=order)

@friends.route('/request', methods=["GET", "POST"])
@login_required
def friends_request():
    if request.method == "POST":
        userid = request.form["userid"]
        user = db.session.query(User).filter(User.id == userid).first()
    return render_template('friends/request.html', user=user)

@friends.route('/request/com',methods=["GET", "POST"])
@login_required
def friends_request_com():
    if request.method == "POST":
        friendid = request.form["userid"]
        friend = Friends(
            user_id = current_user.id,
            friend_id = friendid,
            status = False,
            recipient = friendid,
            room_ID = "_".join(sorted([str(current_user.id),str(friendid)]))
        )
        db.session.add(friend)
        db.session.commit()
        friend = Friends(
            user_id = friendid,
            friend_id = current_user.id,
            status = False,
            recipient = friendid,
            room_ID = "_".join(sorted([str(current_user.id),str(friendid)]))
        )
        db.session.add(friend)
        db.session.commit()
        return redirect(url_for("friends.search"))

@friends.route('/')
@login_required
def friends_function():
    return render_template('friends/index.html')

@friends.route('/requests')
@login_required
def friends_requests():
    friends_id = [row[0] for row in db.session.query(Friends.user_id).filter(and_(Friends.recipient == current_user.id,
                                                                                    Friends.user_id != current_user.id,
                                                                                    Friends.status == False)).all()]
    users = db.session.query(User).filter(User.id.in_(friends_id)).all()
    return render_template('friends/requests.html', users=users)

@friends.route('/requests/permission',methods=["GET", "POST"])
@login_required
def friends_requests_permission():
    if request.method == "POST":
        userid = request.form["userid"]
        friend = db.session.query(Friends).filter(and_(Friends.friend_id == userid,
                                                  Friends.user_id == current_user.id)).first()
        friend.status = True
        db.session.commit()
        friend = db.session.query(Friends).filter(and_(Friends.user_id == userid,
                                                  Friends.friend_id == current_user.id)).first()
        friend.status = True
        db.session.commit()
        return redirect(url_for("friends.friends_requests"))
@friends.route('/requests/rejection',methods=["GET", "POST"])
@login_required
def friends_requests_rejection():
    if request.method == "POST":
        userid = request.form["userid"]
        db.session.query(Friends).filter(and_(Friends.friend_id == userid,
                                              Friends.user_id == current_user.id)).delete()
        db.session.commit()
        db.session.query(Friends).filter(and_(Friends.user_id == userid,
                                              Friends.friend_id == current_user.id)).delete()
        db.session.commit()
        return redirect(url_for("friends.friends_requests"))
    

@friends.route('/list')
@login_required
def friends_list():
    friends_id = [row[0] for row in db.session.query(Friends.friend_id).filter(and_(Friends.user_id == current_user.id,
                                                                                    Friends.status == True)).all()]
    users = db.session.query(User).filter(User.id.in_(friends_id)).all()
    return render_template('friends/list.html', users=users)

@friends.route('/delete',methods=["GET", "POST"])
@login_required
def friends_delete():
    if request.method == "POST":
        userid = request.form["userid"]
        user = db.session.query(User).filter(User.id == userid).first()
    return render_template('friends/delete.html', user=user)

@friends.route('/delete/com',methods=["GET", "POST"])
@login_required
def friends_delete_com():
    if request.method == "POST":
        friendid = request.form["userid"]
        db.session.query(Friends).filter(and_(Friends.friend_id == friendid,
                                            Friends.user_id == current_user.id)).delete()
        db.session.commit()
        db.session.query(Friends).filter(and_(Friends.user_id == friendid,
                                            Friends.friend_id == current_user.id)).delete()
        db.session.commit()
        return render_template('friends/delete_com.html')