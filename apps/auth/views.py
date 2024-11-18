from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.auth.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, login_required, logout_user

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

@auth.route("/auth_ok")
@login_required
def auth_ok():
    return render_template("auth/index.html")

# signupエンドポイントを作成する
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # SignUpFormをインスタンス化
    signform = SignUpForm()
    if signform.validate_on_submit():
        user = User(
            username = signform.username.data,
            email = signform.email.data,
            password = signform.password.data,
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
            next_ = url_for("auth.auth_ok")
        return redirect(next_)
    
    return render_template("auth/signup.html", form=signform)

# loginエンドポイントを作成する
@auth.route("/login", methods=["GET", "POST"])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        # メールアドレスからユーザー取得
        user = User.query.filter_by(email=loginform.email.data).first()
        # ユーザーが存在しパスワード一致ならログイン許可
        if user is not None and user.verify_password(loginform.password.data):
            login_user(user)
            return redirect(url_for("auth.auth_ok"))
        # ログイン失敗メッセージを設定する
        flash("メールアドレスかパスワードが不正です")
        
    return render_template("auth/login.html", form=loginform)

# logoutエンドポイントを作成する
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))