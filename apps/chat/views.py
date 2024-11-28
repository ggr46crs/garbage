from apps.app import db,socketio,app
from sqlalchemy import or_,and_,not_
from apps.auth.models import User
from apps.friends.models import Friends
from apps.chat.models import Chat
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user,current_user
from flask_socketio import SocketIO, emit
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

@chat.route("/chatroom",methods=["GET", "POST"])
def chatroom():
    if request.method == "POST":
        friend_id = request.form["userid"]
        chat = db.session.query(Chat).filter(or_(
            and_(Chat.send == current_user,
                 Chat.receive == friend_id),
            and_(Chat.send == friend_id,
                 Chat.receive == current_user))).order_by(Chat.data).all()
        friend_name = db.session.query(User.username).filter(User.id == friend_id).first()
        return render_template('chat/chatroom.html',chat=chat,friend_name=friend_name)

@chat.route('/')
def index():
    return render_template('chat/index2.html')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    emit('message', msg, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app)


