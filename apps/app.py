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
# flask_socketio追加
from flask_socketio import SocketIO, emit
# SQLAlchemyのインスタンス作成
db = SQLAlchemy()

login_manager = LoginManager()
# login_view属性に未ログイン時にリダイレクトするエンドポイントを指定
login_manager.login_view = "auth.signup"
# login_message属性にログイン後に表示するメッセージを指定
# ここでは何も表示しないよう空を指定
login_manager.login_message = ""
socketio = SocketIO()
app = ""

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
    # flask_socketio追加
    global socketio
    socketio = SocketIO(app)
    socketio.init_app(app)

    # authパッケージからviewsをインポート
    from apps.auth import views as auth_views
    from apps.chat import views as chat_views
    from apps.friends import views as friends_views
    from apps.crud import views as crud_views

    # register_blueprintを利用してviewsのauthappをアプリへ登録
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    app.register_blueprint(chat_views.chat, url_prefix="/chat")
    app.register_blueprint(friends_views.friends, url_prefix="/friends")
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    return app