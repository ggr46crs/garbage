from apps.app import db
from sqlalchemy import or_,and_
from apps.auth.forms import SignUpForm, LoginForm
from apps.auth.models import User
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
def search():
    text_input = request.args.get('search')
    if text_input is None or len(text_input) == 0:
        users = db.session.query(User).filter(User.place1 == current_user.place1,User.id != current_user.id).all()
    else:
        users = db.session.query(User).filter(and_(User.place1 == current_user.place1,or_(User.username.like("%"+text_input+"%"), User.email.like("%"+text_input+"%"))),User.id != current_user.id).all()
    return render_template('friends/search.html', users=users)