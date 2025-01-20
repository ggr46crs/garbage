# flask_wtfからFlaskFormクラスをインポート
from flask_wtf import FlaskForm
# wtformsから各フィールドをインポート
from wtforms import PasswordField, StringField, SubmitField, IntegerField
# wtformsから各バリデータをインポート
from wtforms.validators import DataRequired, Email, Length,Regexp

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
    place = StringField(
        "郵便番号",
        validators = [
            DataRequired("郵便番号は必須です。"),
            Length(7, 7, "郵便番号は7文字以内で入力してください。"),
            Regexp(r'^[0-9]+$', message="郵便番号は半角数字で入力してください。"),
        ]
    )
    submit = SubmitField("新規登録")

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
    submit = SubmitField("ログイン")