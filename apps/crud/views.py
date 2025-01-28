from apps.app import db
from sqlalchemy import or_,and_,not_,create_engine, Column, Integer, String, DateTime, func, extract, Date, cast
from apps.crud.forms import GarbageForm
from apps.auth.models import User
from apps.friends.models import Friends
from apps.chat.models import Chat
from apps.crud.models import GarbageRecord,Garbage
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user,current_user
from datetime import datetime, timedelta
import requests
import calendar
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
@login_required
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
    
    all_months = sorted(garbage_data.keys())  # ソートされた月リスト
    # 選択された月を取得
    selected_month = request.form.get('month')
    if not selected_month:
        if all_months:
            selected_month = max(all_months)  # データが存在する場合は最新月を選択
        else:
            selected_month = None  # データがない場合

    # データが空の場合の対応
    if not garbage_data or selected_month is None:
        return render_template('crud/chart.html', graph_url=None, months=[], selected_month=None, garbage_counts=[])
    
    # 空のデータを補完（最小月～最大月の範囲でデータがない月に空データを追加）
    min_month = datetime.strptime(min(all_months), '%Y-%m')
    max_month = datetime.strptime(max(all_months), '%Y-%m')
    current_month = min_month
    while current_month <= max_month:
        month_str = current_month.strftime('%Y-%m')
        if month_str not in garbage_data:
            garbage_data[month_str] = {}  # データのない月に空データを追加
        current_month += timedelta(days=calendar.monthrange(current_month.year, current_month.month)[1])

    all_months = sorted(garbage_data.keys())
    
    current_date = datetime.strptime(selected_month, '%Y-%m')  # 文字列をdatetime型に変換
    previous_month = (
        (current_date - timedelta(days=current_date.day)).strftime('%Y-%m')
        if selected_month != min(all_months) else None  # 最小月の場合はNone
    )
    next_month = (
        (current_date + timedelta(days=calendar.monthrange(current_date.year, current_date.month)[1])).strftime('%Y-%m')
        if selected_month != max(all_months) else None  # 最大月の場合はNone
    )
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
    return render_template(
        'crud/chart.html',
        graph_url=graph_url,
        months=garbage_data.keys(),
        selected_month=selected_month,
        garbage_counts=garbage_counts,
        previous_month=previous_month,
        next_month=next_month
    )

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
    
    # 最新月のデータを取得
    garbage_data = {}
    for month, garbage_name, total_amount in garbage_record:
        if month not in garbage_data:
            garbage_data[month] = {}
        garbage_data[month][garbage_name] = float(total_amount)
    
    all_months = sorted(garbage_data.keys())  # ソートされた月リスト
    # 選択された月を取得
    selected_month = request.form.get('month')
    if not selected_month:
        if all_months:
            selected_month = max(all_months)  # データが存在する場合は最新月を選択
        else:
            selected_month = None  # データがない場合

    # データが空の場合の対応
    if not garbage_data or selected_month is None:
        return render_template('crud/friend_chart.html',
                                graph_url=None, months=[],
                                selected_month=None,
                                garbage_counts=[],
                                friend_id=friend_id,
                                friend_name=friend.username)
    
    # 空のデータを補完（最小月～最大月の範囲でデータがない月に空データを追加）
    min_month = datetime.strptime(min(all_months), '%Y-%m')
    max_month = datetime.strptime(max(all_months), '%Y-%m')
    current_month = min_month
    while current_month <= max_month:
        month_str = current_month.strftime('%Y-%m')
        if month_str not in garbage_data:
            garbage_data[month_str] = {}  # データのない月に空データを追加
        current_month += timedelta(days=calendar.monthrange(current_month.year, current_month.month)[1])

    all_months = sorted(garbage_data.keys())
    
    current_date = datetime.strptime(selected_month, '%Y-%m')  # 文字列をdatetime型に変換
    previous_month = (
        (current_date - timedelta(days=current_date.day)).strftime('%Y-%m')
        if selected_month != min(all_months) else None  # 最小月の場合はNone
    )
    next_month = (
        (current_date + timedelta(days=calendar.monthrange(current_date.year, current_date.month)[1])).strftime('%Y-%m')
        if selected_month != max(all_months) else None  # 最大月の場合はNone
    )
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
    return render_template(
        'crud/friend_chart.html',
        graph_url=graph_url,
        months=garbage_data.keys(),
        selected_month=selected_month,
        garbage_counts=garbage_counts,
        friend_id=friend_id,
        friend_name=friend.username,
        previous_month=previous_month,
        next_month=next_month
    )

