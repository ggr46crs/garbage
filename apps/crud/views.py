from apps.app import db
from sqlalchemy import or_,and_,not_
from apps.crud.forms import GarbageForm
from apps.auth.models import User
from apps.friends.models import Friends
from apps.chat.models import Chat
from apps.crud.models import GarbageRecord,Garbage
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user,current_user
import requests
 
crud = Blueprint(
    "crud",
    __name__,
    template_folder = "templates",
    static_folder = "static",
)
 
@crud.route('/')
def crud_function():
    return render_template('crud/index.html')
 
@crud.route("/regist", methods=["GET", "POST"])
def garbage_regist():
    garbageform = GarbageForm()
    garbage_types = db.session.query(Garbage.garbage_code, Garbage.type).all()
    garbageform.garbagecode.choices = [(g[0], g[1]) for g in garbage_types]
    if garbageform.validate_on_submit():
        garbage = GarbageRecord(
            user_id = current_user.id,
            garbage_code = garbageform.garbagecode.data,
            amount = garbageform.amount.data,
            date = garbageform.date.data
        )
        db.session.add(garbage)
        db.session.commit()
        return redirect(url_for("crud.garbage_regist"))
    return render_template("crud/regist.html", form=garbageform)