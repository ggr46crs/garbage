from apps.app import db
from sqlalchemy import or_,and_,not_,create_engine, Column, Integer, String, DateTime, func, extract, Date, cast
from apps.crud.forms import GarbageForm
from apps.auth.models import User
from apps.friends.models import Friends
from apps.chat.models import Chat
from apps.crud.models import GarbageRecord,Garbage
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user,current_user
import requests
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import japanize_matplotlib
from io import BytesIO
import base64
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
 
crud = Blueprint(
    "crud",
    __name__,
    template_folder = "templates",
    static_folder = "static",
)
 
@crud.route('/')
@login_required
def crud_function():
    return render_template('crud/index.html')
 
@crud.route("/regist", methods=["GET", "POST"])
@login_required
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
        return redirect(url_for("crud.crud_regist_complete"))
    return render_template("crud/regist.html", form=garbageform)

@crud.route("/regist/complete", methods=["GET", "POST"])
def crud_regist_complete():
    return render_template("crud/crud_com.html")

@crud.route('/chart', methods=["GET", "POST"])
@login_required
def chart():
    garbage_record = db.session.query(
    func.to_char(func.cast(GarbageRecord.date, Date), 'YYYY-MM').label('month'),
    Garbage.type.label('garbage_name'),
    func.sum(GarbageRecord.amount).label('total_amount')
    ).join(
        Garbage, cast(GarbageRecord.garbage_code, String) == cast(Garbage.garbage_code, String)  # データ型を統一
    ).filter(
        GarbageRecord.user_id == current_user.id
    ).group_by(
        func.to_char(func.cast(GarbageRecord.date, Date), 'YYYY-MM'),
        Garbage.type
    ).all()
 
    # 最新月のデータを取得
    garbage_data = {}
    for month, garbage_name, total_amount in garbage_record:
        if month not in garbage_data:
            garbage_data[month] = {}
        garbage_data[month][garbage_name] = float(total_amount)
 
     # 選択された月の取得
    selected_month = request.form.get('month') or max(garbage_data.keys())
 
    # 指定月のデータを取得
    labels = garbage_data[selected_month].keys()  # ゴミの名前をラベルに
    sizes = garbage_data[selected_month].values()
 
   # ゴミの個数データを作成
    garbage_counts = [{"name": name, "count": int(count)} for name, count in zip(labels, sizes)]
 
    # 円グラフの作成
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
 
    # 画像をbase64エンコード
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
 
    # 月のリストをテンプレートに渡す
    return render_template('crud/chart.html', graph_url=graph_url, months=garbage_data.keys(), selected_month=selected_month, garbage_counts=garbage_counts)

@crud.route('/friend/chart',methods=["GET", "POST"])
@login_required
def friend_chart():
    if request.method == "POST":
        friend_id = request.form["userid"]
    friend = db.session.query(User).filter(User.id == friend_id).first()
    garbage_record = db.session.query(
    func.to_char(func.cast(GarbageRecord.date, Date), 'YYYY-MM').label('month'),
    Garbage.type.label('garbage_name'),
    func.sum(GarbageRecord.amount).label('total_amount')
    ).join(
        Garbage, cast(GarbageRecord.garbage_code, String) == cast(Garbage.garbage_code, String)  # データ型を統一
    ).filter(
        GarbageRecord.user_id == friend_id
    ).group_by(
        func.to_char(func.cast(GarbageRecord.date, Date), 'YYYY-MM'),
        Garbage.type
    ).all()

    if not garbage_record:
        return render_template('crud/friend_chart.html', graph_url=None, months=[], selected_month=None, garbage_counts=[])
    # 最新月のデータを取得
    garbage_data = {}
    for month, garbage_name, total_amount in garbage_record:
        if month not in garbage_data:
            garbage_data[month] = {}
        garbage_data[month][garbage_name] = float(total_amount)
 
    # 選択された月の取得
    selected_month = request.form.get('month') or max(garbage_data.keys())
 
    # 指定月のデータを取得
    labels = garbage_data[selected_month].keys()  # ゴミの名前をラベルに
    sizes = garbage_data[selected_month].values()
 
   # ゴミの個数データを作成
    garbage_counts = [{"name": name, "count": int(count)} for name, count in zip(labels, sizes)]
 
    # 円グラフの作成
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
 
    # 画像をbase64エンコード
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
 
    # 月のリストをテンプレートに渡す
    return render_template('crud/friend_chart.html', graph_url=graph_url, months=garbage_data.keys(), selected_month=selected_month, garbage_counts=garbage_counts,friend_id=friend_id,friend_name=friend.username)

