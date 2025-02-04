from flask_wtf import FlaskForm
from wtforms import SubmitField,SelectField,IntegerField,DateField
from wtforms.validators import length,DataRequired,NumberRange,ValidationError
from datetime import date


class GarbageForm(FlaskForm):
    garbagecode = SelectField(
        "ごみの種類",
        choices=[],
        validators=[
            DataRequired(message="ごみの種類を選択してください"),
            ]
    )
    amount = IntegerField(
        "ごみの量",
        validators=[
            NumberRange(min=1,message="正の整数を入力してください"),
            DataRequired(message="ごみの量は必須です"),
        ]
    )
    date = DateField(
        "日付",
        validators=[
            DataRequired(message="日付は必須です"),
        ]
    )
    submit = SubmitField("登録")

    def validate_date(self, field):
        if field.data > date.today():
            raise ValidationError("明日以降の日付は入力できません。")