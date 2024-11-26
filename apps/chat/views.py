from apps.app import db
from sqlalchemy import or_,and_,not_
from apps.auth.models import User
from apps.friends.models import Friends
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user,current_user
import requests

chat = Blueprint(
    "chat",
    __name__,
    template_folder = "templates",
    static_folder = "static",
)

@chat.route("/userlist")
def userlist():
    friends_id = [row[0] for row in db.session.query(Friends.friend_id).filter(and_(Friends.user_id == current_user.id,
                                                                                    Friends.status == True)).all()]
    users = db.session.query(User).filter(User.id.in_(friends_id)).all()
    return render_template('chat/index.html', users=users)

