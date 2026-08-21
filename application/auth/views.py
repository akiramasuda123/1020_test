"""
参考
・Flask本格入門やさしくわかるWebアプリ開発：P312
・Python FlaskによるWebアプリ開発入門：P142~162
"""

from flask import Blueprint, render_template, flash, url_for, redirect, request
from models import db, LoginUser
from application.auth.forms import SignupForm as SignUpForm, LoginForm
from flask_login import login_user, logout_user

# Blueprintを使ってauthを生成（templatesとstaticフォルダを指定）
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# サインアップ（新規ユーザー登録）================================================================================
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # SignUpFormをインスタンス化
    form = SignUpForm()

    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():

        # フォームの入力値からUserモデルのインスタンスを作成する
        user = LoginUser(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
    
        # ユーザー情報をDBに登録する
        db.session.add(user)
        db.session.commit()

        # フラッシュメッセージ
        flash("ユーザーを登録しました")

        # ログイン画面へ移行
        return redirect(url_for("auth.login"))

    # バリデーション失敗時はサインアップページを再表示
    return render_template("auth/signup.html", form=form)
# ===========================================================================================================

# ログイン============================================================================
@auth.route("/login", methods=["GET", "POST"])
def login():
    
    # LoginFormをインスタンス化
    form = LoginForm()

   # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        
        # フォームの入力値を変数に格納
        username = form.username.data
        password = form.password.data
        
        # ユーザー名でユーザーを検索する
        user = LoginUser.query.filter_by(username=username).first()

        # ユーザーが存在し、パスワードが一致する場合はログイン処理を行う
        if user is not None and user.verify_password(password):
            # userを渡して、ログイン状態にする
            login_user(user)
            return redirect(url_for("home"))

        # ログイン失敗時のエラーメッセージを設定
        flash("ユーザー名またはパスワードが異なります")

    return render_template("auth/login.html", form=form)
# =======================================================================================

# ログアウト==============================================================================
@auth.route("/logout")
def logout():
    # セッションからユーザー情報を削除してログアウト
    logout_user()
    # フラッシュメッセージ
    flash("ログアウトしました")
    # ログインページへリダイレクト
    return redirect(url_for("auth.login"))
# ========================================================================================
