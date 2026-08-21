"""
参考
・Flask本格入門やさしくわかるWebアプリ開発（教科書）P274
・Python FlaskによるWebアプリ開発入門（教科書）P133
"""

# アプリの設定ファイル
from pathlib import Path

# プロジェクトのルートディレクトリを取得
basedir = Path(__file__).parent


class Config(object):
    
    # デバックモード
    DEBUG = True
    # セッションやCSRF保護に使用するシークレットキー
    SECRET_KEY = "2AZSMss3p5QPbcY2hBsJ"
    # SQLiteデータベースのURIを設定する
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'library.sqlite'}"
    # WTFormsのCSRF保護に使用するシークレットキー
    WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"
    # SQLAlchemyの変更追跡機能を無効化（不要な警告を防ぐ）
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLAlchemyのクエリログを有効にする（開発時のデバッグ用）
    SQLALCHEMY_ECHO = True