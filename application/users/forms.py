from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, ValidationError
from models import User

# 利用者登録・編集フォーム============================================
class UserForm(FlaskForm):

    # 編集時に自分自身を除外するためのID（登録時はNone）
    # 編集時のメールアドレス重複してますの対策
    user_id = None

    # 利用者名の入力欄
    name = StringField(
        "ユーザー名",
        validators=[
            DataRequired("ユーザー名は必須です"),
        ],
    )

    # メールアドレスの入力欄（必須・メール形式チェック）
    email = EmailField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です"),
            Email("メールアドレスの形式で入力してください"),
        ],
    )

    # 登録ボタン
    submit = SubmitField("保存")
    
    
    # カスタムバリデータエラーを作成（同じメールアドレスが使用されていないかチェック）
    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        # 取得したユーザーが存在し、かつ自分自身でない場合（編集対策）
        if user and user.user_id != self.user_id:
            raise ValidationError("このメールアドレスは使用されています")
        
# ===============================================================

"""
・Python FlaskによるWebアプリ開発入門：P237
"""
# 削除フォーム====================================================
class DeleteForm(FlaskForm):
    submit = SubmitField("削除")
# ===============================================================