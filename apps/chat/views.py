from apps.app import db,socketio,app
from sqlalchemy import or_,and_,not_
from apps.auth.models import User
from apps.friends.models import Friends
from apps.chat.models import Chat
from flask import Blueprint, render_template, flash, url_for, redirect, request,jsonify
from flask_login import login_user, login_required, logout_user,current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
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
        
        friend = db.session.query(Friends).filter(and_(Friends.user_id == current_user.id,
                                                       Friends.friend_id == friend_id)).first()
        user = db.session.query(User).filter(User.id == current_user.id).first()
        chats = db.session.query(Chat).filter(or_(
            and_(Chat.send == current_user.id,Chat.receive == friend_id),
            and_(Chat.send == friend_id,Chat.receive == current_user.id))).order_by(Chat.data).all()
        chat_list = [[chat.id,chat.send,chat.receive,chat.comment,chat.data] for chat in chats]
        user_list = [user.id,user.username]
        friend_list = [friend.friend_id,friend.room_ID]
        return render_template('chat/chatroom.html',friend=friend_list,user=user_list,chat=chat_list)
    return redirect(url_for('chat.userlist'))

@chat.route('/')
def index():
    return render_template('chat/chatroom.html')

@socketio.on('join')
def join(msg):
    join_room(msg["room"])

@socketio.on('leave')
def leave(msg):
    leave_room(str(msg["room"]))

@socketio.on('message')
def send_Message(data):
    chat = Chat(
        send = data[3],
        receive = data[2],
        comment = data[0],
    )
    db.session.add(chat)
    db.session.commit()
    print('Message: ' + data[0])
    emit("message",data[0],to=data[1],include_self=False)

if __name__ == '__main__':
    socketio.run(app)


