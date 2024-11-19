# flask_wtfからFlaskFormクラスをインポート
from flask_wtf import FlaskForm
# wtformsから各フィールドをインポート
from wtforms import PasswordField, StringField, SubmitField, IntegerField
# wtformsから各バリデータをインポート
from wtforms.validators import DataRequired, Email, Length

# サインアップフォームクラス作成
class SignUpForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators = [
            DataRequired("ユーザー名は必須です。"),
            Length(1, 30, "30文字以内で入力してください。"),
        ],
    )
    email = StringField(
        "メールアドレス",
        validators = [
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレス形式で入力してください。"),
        ],
    )
    password = PasswordField(
        "パスワード",
        validators = [
            DataRequired("パスワードは必須です。"),
        ],
    )
    # 追加
    place = IntegerField(
        "郵便番号",
        validators = [
            DataRequired("郵便番号は必須です。")
        ]
    )
    submit = SubmitField("Sign up")

# ログインフォームクラス作成
class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators = [
            DataRequired("メールアドレスは必須です。"),
            Email("メールアドレス形式で入力してください。"),
        ],
    )
    password = PasswordField(
        "パスワード",
        validators = [
            DataRequired("パスワードは必須です。"),
        ],
    )
    submit = SubmitField("Login")