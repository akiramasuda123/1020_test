
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from models import LoginUser

"""
・Flask本格入門やさしくわかるWebアプリ開発：P293
・Python FlaskによるWebアプリ開発入門：P148,156
"""
# 新規ユーザー登録フォーム================================================
class SignupForm(FlaskForm):

    # ユーザー名の入力欄（必須・30文字以内）
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired("ユーザー名は必須です"),
            Length(1, 30, "30文字以内で入力してください"),
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

    # パスワードの入力欄（必須）
    password = PasswordField(
        "パスワード",
        validators=[
            Length(5, 20, ""),
            DataRequired("パスワードは必須です"),
        ],
    )

    # 登録ボタン
    submit = SubmitField("新規登録")
    
    # カスタムバリデータエラーを作成（英数字と記号が含まれているかチェックする）
    def validate_password(self, password):
        # アルファベット・数字・記号
        if not (any(c.isalpha() for c in password.data) and \
            any(c.isdigit() for c in password.data) and \
            any(c in '!@#$%^&*()' for c in password.data)):
            raise ValidationError("パスワードは英数字と記号【!@#$%^&*()】のみで入力")
    
    # カスタムバリデータエラーを作成（同じメールアドレスが使用されていないかチェック）
    def validate_email(self,email):
        email = LoginUser.query.filter_by(email=self.email.data).first()
        if email:
            raise ValidationError("このメールアドレスは使用されています")

    # カスタムバリデータエラーを作成（同じメールアドレスが使用されていないかチェック）
    def validate_username(self,username):
        username = LoginUser.query.filter_by(username=self.username.data).first()
        if username:
            raise ValidationError("このユーザー名は使用されています")
# ======================================================================

# ログインフォーム=======================================================
class LoginForm(FlaskForm):

    # ユーザー名の入力欄（必須・30文字以内）
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired("ユーザー名は必須です"),
            Length(1, 30, "30文字以内で入力してください"),
        ],
    )

    # パスワードの入力欄（必須）
    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です"),
        ],
    )

    # ログインボタン
    submit = SubmitField("ログイン")
# =====================================================================