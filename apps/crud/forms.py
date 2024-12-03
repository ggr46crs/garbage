from flask_wtf import FlaskForm
from wtforms import SubmitField,SelectMultipleField,IntegerField,DateField
from wtforms.validators import length,DataRequired

class GarbageForm(FlaskForm):
    garbage_code = SelectMultipleField(
        "ゴミの種類",
        validators=[
            DataRequired(message="ごみの種類を選択してください"),
            ],
    )

    amount = IntegerField(
        "ゴミの量",
        validators=[
            DataRequired(message="ゴミの量は必須ですは必須です"),
        ]
    )
    date = DateField(
        "日付",
        validators=[
            DataRequired(message="日付は必須です"),
        ]
    )
    submit = SubmitField("登録")
