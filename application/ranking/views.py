from flask import Blueprint, render_template
from flask_login import login_required
from models import db, User, Book,BookGenre

# Blueprintの設定
ranking = Blueprint(
    "ranking",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# ランキングの取り出し============================================================================
@ranking.route("/ranking_list")
@login_required
def ranking_list():
    
    """
    ・Flask本格入門やさしくわかるWebアプリ開発：p175（order_byの使い方）
    ・limitを使って、上位5位だけ取り出す：https://qiita.com/Bashi50/items/7f2214550e80b87fb922
    """
    # 利用者の貸出数の多い順に並べて全件取り出し（貸出回数が1以上のみ）
    users = User.query.filter(User.user_borrowed_count > 0).order_by(User.user_borrowed_count.desc()).limit(5).all()
    
    # 本の貸出数の多い順に並べて全件取り出し（貸出回数が1以上のみ）
    books = Book.query.filter(Book.book_borrowed_count > 0).order_by(Book.book_borrowed_count.desc()).limit(5).all()
    
    # ジャンルの貸出数の多い順に並べて全件取り出し（貸出回数が1以上のみ）
    genres = BookGenre.query.filter(BookGenre.genre_borrowed_count > 0).order_by(BookGenre.genre_borrowed_count.desc()).limit(5).all()
    
    # 取得した情報をテンプレートに渡す
    return render_template("ranking/ranking.html", users=users, books=books,genres=genres)
# ===================================================================================