from flask import Blueprint, render_template, redirect, url_for,flash
from flask_login import login_required
from models import db,BookGenre
from application.book_genres.forms import GenreForm,DeleteForm
from application.kyotu import pagination

# Blueprintの設定
book_genres = Blueprint(
    "book_genres",
    __name__,
    template_folder="templates",
    static_folder="static",
)

"""
・Flask本格入門やさしくわかるWebアプリ開発：P315（CRUD機能：一覧表示）
"""
# ジャンル一覧============================================================================
@book_genres.route("/book_genres_list")
@login_required
def book_genres_list():
    
    # DBからジャンル一覧を全件取得
    book_genres = BookGenre.query.all()
    
    # DeleteFormクラスをインスタンス化
    form = DeleteForm()
    
    # ページネーション処理
    book_genres_pag,page,total_pages = pagination(book_genres)
    
    # 取得したジャンルの情報をテンプレートに渡す
    return render_template("book_genres/list.html",
                           book_genres_all=book_genres,
                           book_genres=book_genres_pag,
                           page=page,
                           total_pages=total_pages,
                           form=form)
# ===================================================================================

"""
・Flask本格入門やさしくわかるWebアプリ開発：P315（CRUD機能：登録）
"""
# ジャンルの登録==============================================================================
@book_genres.route("/book_genres_new", methods=["GET", "POST"])
@login_required
def book_genres_new():
    
    # GenreFormクラスをインスタンス化
    form = GenreForm()
    
   # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        
        # 入力されたジャンルをDBに追加
        book_genre = BookGenre(
            genre_name=form.genre_name.data,
        )
        db.session.add(book_genre)
        db.session.commit()
        
        # 完了したらジャンルの一覧へリダイレクト
        return redirect(url_for("book_genres.book_genres_list"))
    
    # フォームをテンプレートに渡す
    return render_template("book_genres/new.html", form=form)
# =======================================================================================

"""
・Flask本格入門やさしくわかるWebアプリ開発：P316（CRUD機能：更新）
"""
# ジャンルの編集（更新）=================================================================================
@book_genres.route("/book_genres_list/<int:id>/update", methods=["GET", "POST"])
@login_required
def book_genres_update(id):
    
    # DBから指定されたidのジャンル情報を取得（見つからない場合は、404エラー）
    book_genre = BookGenre.query.get_or_404(id)
    # bookFormクラスをインスタンス化（入力されている内容を保持して）
    form = GenreForm(obj=book_genre)
    
    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        
        # 入力されたジャンルをDBに置き換える（更新）
        book_genre.genre_name = form.genre_name.data
        db.session.commit()
        
        # 完了したらジャンルの一覧へリダイレクト
        return redirect(url_for("book_genres.book_genres_list"))
    
    # フォームをテンプレートに渡す
    return render_template("book_genres/update.html", form=form)
# ===========================================================================================


"""
・Flask本格入門やさしくわかるWebアプリ開発：P316（CRUD機能：削除）
・Python FlaskによるWebアプリ開発入門：P237~240（forms.pyを利用した削除）
"""
# ジャンルの削除====================================================================================
@book_genres.route("/book_genres_list/<int:id>/delete", methods=["POST"])
@login_required
def book_genres_delete(id):
    
    # DBから指定されたidのジャンルの情報を取得（見つからない場合は、404エラー）
    book_genre = BookGenre.query.get_or_404(id)
    
    # DeleteFormクラスをインスタンス化
    form = DeleteForm()
    
    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        # 指定されたidのジャンルの情報を削除
        db.session.delete(book_genre)
        db.session.commit()
        
        # フラッシュメッセージ
        flash(f"{book_genre.genre_name}を削除しました。")
        
        # 完了したらジャンルの一覧へリダイレクト
        return redirect(url_for("book_genres.book_genres_list"))
    
    # フォームをテンプレートに渡す
    return render_template("book_genres/list.html",form=form)
# ==============================================================================================