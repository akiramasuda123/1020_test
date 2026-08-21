from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField,DateField
from wtforms.validators import DataRequired, NumberRange,ValidationError
from datetime import date

# 新規貸出フォーム============================================
class BorrowForm(FlaskForm):
    
    # 利用者欄
    user_id = SelectField(
        "利用者",
        coerce=int,
        validators=[DataRequired("利用者は必須です")]
    )
    
    # 本欄
    book_id = SelectField(
        "本",
        coerce=int,
        validators=[DataRequired("本は必須です")],
    )
    
    # 返却予定日
    # バリデータで、今日より前の日を入れらないようにする
    due_date = DateField(
        "返却予定日",
        validators=[DataRequired("返却予定日は必須です")]
    )   
    
    submit = SubmitField("保存")
    
    # カスタムバリデータエラーを作成（返却予定日が過去日を入力できないようにする）
    def validate_due_date(self, due_date):
        # 入力日が今日の日付より小さい
        if due_date.data < date.today():
            raise ValidationError("返却予定日は本日以降を入力してください")
    
# ===============================================================

"""
・Python FlaskによるWebアプリ開発入門：P237
"""
# 削除フォーム（テスト用）===============================
class DeleteForm(FlaskForm):
    submit = SubmitField("削除")
# ===============================================================

"""
・Python FlaskによるWebアプリ開発入門：P237（削除機能と同じ）
"""
# 返却フォーム====================================================
class ReturnForm(FlaskForm):
    submit = SubmitField("返却")
# ===============================================================
