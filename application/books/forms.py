from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

# 本登録・編集フォーム============================================
class BookForm(FlaskForm):
    
    # タイトル欄
    title = StringField(
        "タイトル",
        validators=[DataRequired("タイトルは必須です")]
    )
    
    # 著者欄
    author = StringField(
        "著者",
        validators=[DataRequired("著者は必須です")]
    )
    
    # ジャンル欄（ジャンルで作成した内容をセレクトボックスで選べるようにする） 
    genre_id = SelectField(
        "ジャンル",
        coerce=int,
        validators=[DataRequired("ジャンルは必須です")]
    )

    # 在庫欄
    stock = IntegerField(
        "在庫",
        validators=[DataRequired("在庫は必須です"), 
                    NumberRange(min=0)
        ],
    )
    
    
    submit = SubmitField("保存")
# ===============================================================

"""
・Python FlaskによるWebアプリ開発入門：P237
"""
# 削除フォーム====================================================
class DeleteForm(FlaskForm):
    submit = SubmitField("削除")
# ===============================================================