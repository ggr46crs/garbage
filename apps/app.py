# Flaskのインポート
from flask import Flask
# SQLAlchemyのインポート
from flask_sqlalchemy import SQLAlchemy
# Migrateのインポート
from flask_migrate import Migrate
# configをインポート
from apps.config import config
# flask-loginのLoginManagerクラスをインポート
from flask_login import LoginManager

# SQLAlchemyのインスタンス作成
db = SQLAlchemy()

login_manager = LoginManager()
# login_view属性に未ログイン時にリダイレクトするエンドポイントを指定
login_manager.login_view = "auth.signup"
# login_message属性にログイン後に表示するメッセージを指定
# ここでは何も表示しないよう空を指定
login_manager.login_message = ""

def create_app(config_key):
    # Flaskのインスタンス作成
    app = Flask(__name__)

    # config_keyにマッチする環境のコンフィグを読み込む
    app.config.from_object(config[config_key])

    # SQLalchemyとアプリを連携
    db.init_app(app)
    # Migrateとアプリを連携
    Migrate(app, db)
    # login_managerとアプリ連携
    login_manager.init_app(app)

    # authパッケージからviewsをインポート
    from apps.auth import views as auth_views

    # register_blueprintを利用してviewsのauthappをアプリへ登録
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    return app