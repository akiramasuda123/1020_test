"""
DBコマンド
・flask db init
・flask db migrate
・flask db upgrade
"""

"""
・参考ページ
・SQLAlchemy使い方１：https://qiita.com/Bashi50/items/e3459ca2a4661ce5dac6
・SQLAlchemy使い方２：https://qiita.com/Bashi50/items/7f2214550e80b87fb922
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

"""
ログインユーザーテーブル参考
・Flask本格入門やさしくわかるWebアプリ開発：P291
・Python FlaskによるWebアプリ開発入門：P150
"""
# ログインユーザーテーブル======================================================================================
class LoginUser(db.Model, UserMixin):

    __tablename__ = "login_users"

    # 主キー（自動採番）
    id = db.Column(db.Integer, primary_key=True)
    # ユーザー名（一意・インデックス付き）
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    # メールアドレス（一意・インデックス付き）
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    # ハッシュ化されたパスワード（平文は保存しない）
    password_hash = db.Column(db.String(255), nullable=False)
    # 作成日時
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 更新日時（更新時に自動で現在時刻をセット）
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    
    @property
    def password(self):
        # パスワードの直接読み取りを禁止する
        raise AttributeError("読み取り不可")

    @password.setter
    def password(self, password):
        # パスワードをハッシュ化してpassword_hashに格納する
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # 入力されたパスワードとハッシュを照合する
        return check_password_hash(self.password_hash, password)

# Flask-Loginがセッションからユーザー情報を復元するための関数
# current_userを復元する
@login_manager.user_loader
def load_user(user_id):
    return LoginUser.query.get(user_id)
# ===============================================================================================

"""
テーブル参考
・Flask本格入門やさしくわかるWebアプリ開発：P198～226
"""
# 利用者テーブル================================================================================
class User(db.Model):
    
    __tablename__ = "users"
    
    # 利用者ID
    user_id = db.Column(db.Integer, primary_key=True)
    # 利用者名
    name = db.Column(db.String(255), nullable=False)
    # メールアドレス
    email = db.Column(db.String(255), nullable=False)
    # ブラックリストフラグ（３回滞納）
    blackflag = db.Column(db.Boolean, nullable=False, default=False)
    # 貸出滞納回数
    overdue_count = db.Column(db.Integer, nullable=False, default=0)
    # 貸出回数
    user_borrowed_count = db.Column(db.Integer, nullable=False, default=0)

# =============================================================================================

# 本テーブル================================================================================
class Book(db.Model):
    
    __tablename__ = "books"
    
    # 本ID
    book_id = db.Column(db.Integer, primary_key=True)
    # タイトル
    title = db.Column(db.String(255), nullable=False)
    # 著者
    author = db.Column(db.String(255), nullable=False)
    # ジャンル
    genre_id = db.Column(db.Integer, db.ForeignKey("book_genres.genre_id"), nullable=False)
    # 在庫冊数
    stock = db.Column(db.Integer, nullable=False)
    # 貸出回数
    book_borrowed_count = db.Column(db.Integer, nullable=False, default=0)

# =============================================================================================

# 本のジャンルテーブル==============================================================================
class BookGenre(db.Model):
    
    __tablename__ = "book_genres"

    # ジャンルID
    genre_id = db.Column(db.Integer, primary_key=True)
    # ジャンル名
    genre_name = db.Column(db.String(255), nullable=False)
    # 貸出回数
    genre_borrowed_count = db.Column(db.Integer, nullable=False, default=0)

# =============================================================================================


# 貸出テーブル================================================================================
class Borrow(db.Model):
    
    __tablename__ = "borrows"
    
    # 貸出ID
    borrows_id = db.Column(db.Integer, primary_key=True)
    # 利用者ID
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    # 本ID
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    # 貸出日
    borrowed_at = db.Column(db.Date, nullable=False,default=date.today)
    # 返却日（NULLの場合は貸出中）
    returned_at = db.Column(db.Date)
    # 返却予定日
    due_date = db.Column(db.Date)
# =============================================================================================