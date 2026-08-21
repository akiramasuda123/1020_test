from flask import Blueprint, render_template, redirect, url_for,flash
from flask_login import login_required
from models import db, Book, BookGenre
from application.books.forms import BookForm,DeleteForm
from application.kyotu import pagination

# Blueprintの設定
books = Blueprint(
    "books",
    __name__,
    template_folder="templates",
    static_folder="static",
)

"""
・Flask本格入門やさしくわかるWebアプリ開発：P315（CRUD機能：一覧表示）
"""
# 本一覧============================================================================
@books.route("/books_list")
@login_required
def books_list():
    
    """
    ・Flask本格入門やさしくわかるWebアプリ開発：p181（joinの使い方）
    """
    # DBから本の情報を全件取得(BookGenreのジャンル名も取得して、ジャンルの表示を工夫する)
    books = db.session.query(Book,BookGenre.genre_name).join(BookGenre, Book.genre_id == BookGenre.genre_id).all()
    
    # DeleteFormクラスをインスタンス化
    form = DeleteForm()
    
    # ページネーション処理
    books_pag,page,total_pages = pagination(books)
    
    # 取得した本の情報をテンプレートに渡す
    return render_template("books/list.html",
                           books_all=books,
                           books=books_pag,
                           page=page,
                           total_pages=total_pages,
                           form=form)
# ===================================================================================


"""
・Flask本格入門やさしくわかるWebアプリ開発：P315（CRUD機能：登録）
"""
# 本の登録==============================================================================
@books.route("/books_new", methods=["GET", "POST"])
@login_required
def books_new():
    
    # bookFormクラスをインスタンス化
    form = BookForm()
    
    """
    DBのデータを選択肢としてセットする方法
    ・choicesのセットの仕方１：https://techblog.hys-neko-lab.com/entry/2022/08/06/165940
    ・choicesのセットの仕方２：https://qiita.com/hahirusan/items/b0b940e5ab2f0a68b2db
    """
    # ジャンル一覧を取得して選択肢にセット
    genres = BookGenre.query.all()
    form.genre_id.choices = [(0, "選択してください")] + [(genre.genre_id, genre.genre_name) for genre in genres]
    
   # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        
        # 入力された本のタイトル、著者、ジャンル、在庫をDBに追加
        book = Book(
            title=form.title.data,
            author=form.author.data,
            genre_id=form.genre_id.data,
            stock=form.stock.data,
        )
        db.session.add(book)
        db.session.commit()
        
        # 完了したら本の一覧へリダイレクト
        return redirect(url_for("books.books_list"))
    
    # フォームをテンプレートに渡す
    return render_template("books/new.html", form=form)
# =======================================================================================


"""
・Flask本格入門やさしくわかるWebアプリ開発：P316（CRUD機能：更新）
"""
# 本の編集（更新）=================================================================================
@books.route("/books_list/<int:id>/update", methods=["GET", "POST"])
@login_required
def books_update(id):
    
    # DBから指定されたidの本の情報を取得（見つからない場合は、404エラー）
    book = Book.query.get_or_404(id)
    # bookFormクラスをインスタンス化（入力されている内容を保持して）
    form = BookForm(obj=book)
    
    """
    DBのデータを選択肢としてセットする方法
    ・choicesのセットの仕方１：https://techblog.hys-neko-lab.com/entry/2022/08/06/165940
    ・choicesのセットの仕方２：https://qiita.com/hahirusan/items/b0b940e5ab2f0a68b2db
    """
    # ジャンル一覧を取得して選択肢にセット
    genres = BookGenre.query.all()
    form.genre_id.choices = [(0, "選択してください")] + [(genre.genre_id, genre.genre_name) for genre in genres]
    
   # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        
        # 入力された本のタイトル、著者、ジャンル、在庫をDBに置き換える（更新）
        book.title = form.title.data
        book.author = form.author.data
        book.genre_id=form.genre_id.data
        book.stock = form.stock.data
        db.session.commit()
        
        # 完了したら本の一覧へリダイレクト
        return redirect(url_for("books.books_list"))
    
    # フォームをテンプレートに渡す
    return render_template("books/update.html", form=form)
# ===========================================================================================

"""
・Flask本格入門やさしくわかるWebアプリ開発：P316（CRUD機能：削除）
・Python FlaskによるWebアプリ開発入門：P237~240（forms.pyを利用した削除）
"""
# 本の削除====================================================================================
@books.route("/books_list/<int:id>/delete", methods=["POST"])
@login_required
def books_delete(id):
    
    # DBから指定されたidの本の情報を取得（見つからない場合は、404エラー）
    book = Book.query.get_or_404(id)
    
    # DeleteFormクラスをインスタンス化
    form = DeleteForm()
    
    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        # 指定されたidの本の情報を削除
        db.session.delete(book)
        db.session.commit()
        
        # フラッシュメッセージ
        flash(f"{book.title}を削除しました。")
    
        # 完了したら本の一覧へリダイレクト
        return redirect(url_for("books.books_list"))
    
    # フォームをテンプレートに渡す
    return render_template("books/list.html", form=form)
# ==============================================================================================