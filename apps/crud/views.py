from apps.app import db
from sqlalchemy import or_,and_,not_
from apps.auth.models import User
from apps.friends.models import Friends
from apps.chat.models import Chat
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user,current_user
import requests

crud = Blueprint(
    "crud",
    __name__,
    template_folder = "templates",
    static_folder = "static",
)
