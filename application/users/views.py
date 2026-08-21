from flask import Blueprint, render_template, redirect, url_for,flash
from flask_login import login_required
from models import db, User
from application.users.forms import UserForm,DeleteForm
from application.kyotu import pagination

# Blueprintの設定
users = Blueprint(
    "users",
    __name__,
    template_folder="templates",
    static_folder="static",
)

"""
・Flask本格入門やさしくわかるWebアプリ開発：P315（CRUD機能：一覧表示）
"""
# 利用者一覧============================================================================
@users.route("/users_list")
@login_required
def users_list():
    # DBから利用者一覧を全件取得
    users = User.query.all()

    # DeleteFormクラスをインスタンス化
    form = DeleteForm()

    # ページネーション処理
    users_pag,page,total_pages = pagination(users)
    
    # 取得した利用者情報をテンプレートに渡す
    return render_template("users/list.html",
                           users_all=users,
                           users=users_pag,
                           page=page,
                           total_pages=total_pages,
                           form=form)
# ===================================================================================


"""
・Flask本格入門やさしくわかるWebアプリ開発：P315（CRUD機能：登録）
"""
# 利用者の登録==============================================================================
@users.route("/users_new", methods=["GET", "POST"])
@login_required
def users_new():
    
    # Userクラスをインスタンス化
    form = UserForm()
    
    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        
        # 入力された利用者名、メールアドレスをDBに追加
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        
        db.session.add(user)
        db.session.commit()
        
        # 完了したら利用者の一覧へリダイレクト
        return redirect(url_for("users.users_list"))
    
    # フォームをテンプレートに渡す
    return render_template("users/new.html", form=form)
# =======================================================================================

"""
・Flask本格入門やさしくわかるWebアプリ開発：P316（CRUD機能：更新）
"""
# 利用者の編集（更新）=================================================================================
@users.route("/users_list/<int:id>/update", methods=["GET", "POST"])
@login_required
def users_update(id):
    
    # DBから指定されたidの利用者情報を取得（見つからない場合は、404エラー）
    user = User.query.get_or_404(id)
    # UserFormクラスをインスタンス化（入力されている内容を保持して）
    form = UserForm(obj=user)
    # 自分自身のIDをセット（メール重複チェックで自分を除外するため）
    form.user_id = user.user_id
    
    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        
        # 入力された利用者名、メールアドレスをDBに置き換える（更新）
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        
        # 完了したらジャンルの一覧へリダイレクト
        return redirect(url_for("users.users_list"))
    
    # フォームをテンプレートに渡す
    return render_template("users/update.html", form=form)
# ===========================================================================================

"""
・Flask本格入門やさしくわかるWebアプリ開発：P316（CRUD機能：削除）
・Python FlaskによるWebアプリ開発入門：P237~240（forms.pyを利用した削除）
"""
# 利用者の削除====================================================================================
@users.route("/users_list/<int:id>/delete", methods=["POST"])
@login_required
def users_delete(id):
    
    # DBから指定されたidの利用者の情報を取得（見つからない場合は、404エラー）
    user = User.query.get_or_404(id)
    
    # DeleteFormクラスをインスタンス化
    form = DeleteForm()
    
    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
    
        # 指定されたidの利用者の情報を削除
        db.session.delete(user)
        db.session.commit()
        
        # フラッシュメッセージ
        flash(f"{user.name}を削除しました。")
        
        # 完了したらジャンルの一覧へリダイレクト
        return redirect(url_for("users.users_list"))
    
    # フォームをテンプレートに渡す
    return render_template("users/list.html", form=form)
# ==============================================================================================