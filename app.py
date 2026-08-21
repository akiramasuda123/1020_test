# 仮想環境コマンド：conda activate flask_env

"""
参考
・Flask本格入門やさしくわかるWebアプリ開発：P257,295,323
"""
from flask import Flask,render_template,g,session
from markupsafe import Markup
from flask_migrate import Migrate
from models import db, login_manager
from flask_login import login_required
from flask_wtf.csrf import CSRFProtect
from models import LoginUser


# Flaskアプリのインスタンス化
app = Flask(__name__)
# 設定ファイル読み込み
app.config.from_object("config.Config")
# dbとFlaskとの紐づけ
db.init_app(app)
# CSRF保護の初期化
csrf = CSRFProtect()
csrf.init_app(app)
# マイグレーションとの紐づけ（Flaskとdb)
migrate = Migrate(app, db)

# login_managerの設定とFlaskアプリへの紐づけ
login_manager.login_view = "auth.login"
login_manager.login_message = "ログインしてください"
login_manager.init_app(app)

"""
Blueprintの登録
・Flask本格入門やさしくわかるWebアプリ開発：P323
・Python FlaskによるWebアプリ開発入門：P144.174
"""
# Blueprintの登録=============================================================================
# auth Blueprint登録
from application.auth import views as auth_views
app.register_blueprint(auth_views.auth, url_prefix="/auth")

# books Blueprint登録
from application.books import views as books_views
app.register_blueprint(books_views.books, url_prefix="/books")

# book_genres Blueprint登録
from application.book_genres import views as book_genres_views
app.register_blueprint(book_genres_views.book_genres, url_prefix="/book_genres")

# users Blueprint登録
from application.users import views as users_views
app.register_blueprint(users_views.users, url_prefix="/users")

# borrows Blueprint登録
from application.borrows import views as borrows_views
app.register_blueprint(borrows_views.borrows, url_prefix="/borrows")

# ranking Blueprint登録
from application.ranking import views as ranking_views
app.register_blueprint(ranking_views.ranking, url_prefix="/ranking")
# ================================================================================================

"""
フィルター、自作フィルター
・Flask本格入門やさしくわかるWebアプリ開発：P104~113
"""
# 自作フィルター=================================================================================

# 自作フィルター（在庫数を受け取り、0なら「在庫なし」と表示）
@app.template_filter('stock_zero')
def stock_zero(value):
    if value == 0:
        return '在庫なし'
    return value

# 自作フィルター（ブラックリストフラグを受け取り、Trueならリストの該当者を黒網掛けにする）
@app.template_filter('create_blacklist')
def create_blacklist(value):
    if value == True:
        
        # Markupを使い、テンプレートにタグ生成させる方法は、AIに聞きました。
        return Markup('<tr style="background-color: black; color: white;">')
    return Markup('<tr>')

# 自作フィルター（日付を受け取り、形式をYY/MM/DDに変更、月や日に0が付く場合は0を消す）
@app.template_filter('date_format')
def date_format(value):
    
    """
    yymmddの参考：https://prograshi.com/language/python/python-change-datetime-output-format/
    """
    return value.strftime('%Y年%#m月%#d日')


# 貸出返却のオレンジや黄色、滞納の赤塗りも自作フィルターでできるが、Markupを利用するため、テンプレートでの記述にしています。
# =============================================================================================

"""
エラーハンドリング
・Flask本格入門やさしくわかるWebアプリ開発：P114~118
"""
# エラーハンドリング============================================================================
# 404エラーハンドリング
@app.errorhandler(404)
def show_404_page(error):
    msg = error.description
    print('エラー内容：',msg)
    return render_template('404.html') , 404

# 500エラーハンドリング
@app.errorhandler(500)
def show_500_page(error):
    print('エラー内容：', error)
    return render_template('500.html') , 500
# =============================================================================================

"""
グローバル変数「g」
・Flask本格入門やさしくわかるWebアプリ開発：P236
・gの利用：https://study-flask.readthedocs.io/ja/latest/04.html
"""
# グローバル変数「g」の活用======================================================================
# 認証機能として、ログインユーザの情報をリクエスト中保持させる

@app.before_request
def load_user():
        
    # sessionに保存したキー名を取得
    # print("セッションの中身:", dict(session))
    user_id = session.get('_user_id')  
    
    if user_id is None:
        # ログインしていない場合は None を設定
        g.user = None
    else:
        # ログイン中であればLoginUserテーブルから値を取得してg.userに格納
        g.user = LoginUser.query.get(user_id)

# ===============================================================================================

# 直接、アプリのリンクへ飛ぶ
@app.route("/")
@login_required
def home():
    return render_template("home.html")
    
# 実行
if __name__ == "__main__":
    app.run(debug=True)
