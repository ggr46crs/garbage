from apps.app import db
from apps.auth.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user
import requests

chat = Blueprint(
    "chat",
    __name__,
    template_folder = "templates",
    static_folder = "static",
)

@chat.route("/userlist")
def userlist():
    db.session.query(User).all()
    return
