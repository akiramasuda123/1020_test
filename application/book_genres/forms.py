from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

# 本のジャンル登録・編集フォーム===================================
class GenreForm(FlaskForm):
    
    # ジャンル入力欄
    genre_name = StringField(
        "ジャンル名",
        validators=[DataRequired("ジャンル名は必須です")]
    )
    
    # 保存ボタン
    submit = SubmitField("保存")
# ==============================================================

"""
・Python FlaskによるWebアプリ開発入門：P237
"""
# 削除フォーム====================================================
class DeleteForm(FlaskForm):
    
    # 削除ボタン
    submit = SubmitField("削除")
# ===============================================================