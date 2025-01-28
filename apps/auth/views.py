from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.auth.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user,current_user
import requests

auth = Blueprint(
    "auth",
    __name__,
    template_folder = "templates",
    static_folder = "static",
)

@auth.route("/")
def index():
    # TOPページへのアクセスはサインアップページに遷移させる
    return redirect(url_for("auth.signup"))
# signupエンドポイントを作成する
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # SignUpFormをインスタンス化
    signform = SignUpForm()
    if current_user.is_authenticated:
        logout_user()
    if signform.validate_on_submit():
        zipcode = signform.place.data
        # 郵便番号検索APIのURLを定数化する
        URL = 'https://zipcloud.ibsnet.co.jp/api/search'
        # paramsで検索したい郵便番号を渡す
        res = requests.get(URL, params={'zipcode': zipcode})
        result = res.json()

        if result['results'] is None:
            signform.place.errors.append("入力された郵便番号は存在しません。")
            return render_template("auth/signup.html", form=signform)

        result = result['results']
        user = User(
            username = signform.username.data,
            email = signform.email.data,
            password = signform.password.data,
            place1 = result[0]['address1'],
            place2 = result[0]['address2'],
        )
        # メールアドレス重複チェック
        if user.is_duplicate_email():
            flash("指定のメールアドレスは登録済みです")
            return redirect(url_for("auth.signup"))
        # ユーザー情報を登録する
        db.session.add(user)
        db.session.commit()
        # ユーザー情報をセッションに格納
        login_user(user)
        # GETパラメータにnextキーが存在し値がない場合にToDo一覧へ
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("crud.crud_function")
        return redirect(next_)
    
    return render_template("auth/signup.html", form=signform)

# loginエンドポイントを作成する
@auth.route("/login", methods=["GET", "POST"])
def login():
    loginform = LoginForm()
    if current_user.is_authenticated:
        logout_user()
    if loginform.validate_on_submit():
        # メールアドレスからユーザー取得
        user = User.query.filter_by(email=loginform.email.data).first()
        # ユーザーが存在しパスワード一致ならログイン許可
        if user is not None and user.verify_password(loginform.password.data):
            login_user(user)
            return redirect(url_for("crud.crud_function"))
        # ログイン失敗メッセージを設定する
        flash("メールアドレスかパスワードが不正です")
        
    return render_template("auth/login.html", form=loginform)

# logoutエンドポイントを作成する
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))