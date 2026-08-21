from flask import Blueprint, render_template, redirect, url_for,request
from flask_login import login_required
from models import db, Borrow,User,Book,BookGenre
from application.borrows.forms import BorrowForm,ReturnForm,DeleteForm
from application.kyotu import pagination
from datetime import date
from flask import flash

# Blueprintの設定
borrows = Blueprint(
    "borrows",
    __name__,
    template_folder="templates",
    static_folder="static",
)

"""
・Flask本格入門やさしくわかるWebアプリ開発：P315（CRUD機能：一覧表示）
"""
# 貸出中一覧============================================================================
@borrows.route("/borrows_active_list/")
@login_required
def borrows_active_list():

    """
    ・DBテーブル内の値がNONEの内容を取り出す方法：https://qiita.com/Bashi50/items/7f2214550e80b87fb922
    ・Flask本格入門やさしくわかるWebアプリ開発：P181（joinの使い方）
    """
    #貸出中（returned_atがNULLのもの）のデータを取得。Userの利用者名と、Bookの本のタイトルも取得
    borrows_active = db.session.query(
        Borrow, User.name, Book.title
        ).join(
            User, Borrow.user_id == User.user_id
            ).join(
                # 本テーブルと貸出テーブルを
                Book, Borrow.book_id == Book.book_id
                ).filter(
                    # 本の返却日がNoneでフィルター
                    Borrow.returned_at.is_(None))

    """
    検索機能
    ・Python FlaskによるWebアプリ開発入門（教科書） P244～249
    参考サイト
    ・likeを使ったあいまい検索：https://ninja-camp.net/flask/223
    ・request.args.getについて：https://iifx.dev/ja/articles/54724471/%E3%81%93%E3%82%8C%E3%81%A7%E5%AE%8C%E7%92%A7-flask%E3%81%A7%E3%81%AE%E3%82%AF%E3%82%A8%E3%83%AA%E6%96%87%E5%AD%97%E5%88%97%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E5%85%A5%E9%96%80%E3%82%AC%E3%82%A4%E3%83%89
    ・検索テンプレート用１：https://ja.python-3.com/?p=389382
    ・検索テンプレート用２：https://qiita.com/yuuki-h/items/171006db887e0427aae2
    """
    # 検索キーワードを取得
    # GETリクエストのURLパラメータ（?search=xxx）から検索キーワードを取得
    # 第一引数：フォームの <input name="search"> の値を取り出す
    # 第二引数：デフォルト値（空文字）
    # 第三引数：取得した値を文字列型に変換
    # .strip()：検索文字列の無駄な空白を消す
    search_keyword = request.args.get("search", "", type=str).strip()

    # ラジオボタンの内容を取得
    # GETリクエストのURLパラメータ（?search_type=xxx）からラジオボタンの選択値を取得
    # 第一引数：フォームの <input name="search_type"> の値を取り出す
    # 第二引数：デフォルト値として「利用者検索（user）」を設定
    # 第三引数：取得した値を文字列型に変換
    search_type = request.args.get("search_type", "user", type=str)

    # 検索キーワードが存在する場合（空文字でない場合）にLIKEであいまい検索
    if search_keyword:
        # ラジオボタンの選択が、本のタイトル
        if search_type == "title":
            # 本のタイトルでのあいまい検索（デフォルト）
            borrows_active = borrows_active.filter(Book.title.like("%" + search_keyword + "%"))
        # ラジオボタンの選択が、利用者名
        else:
            # 利用者名でのあいまい検索
            borrows_active = borrows_active.filter(User.name.like("%" + search_keyword + "%"))

    # 検索フィルター済みの貸出データの全件取得
    borrows_active_all = borrows_active.all()

    # ReturnFormクラスをインスタンス化
    form = ReturnForm()

    # ページネーション処理
    borrows_active_pag, page, total_pages = pagination(borrows_active_all)
    
    # テンプレートへ検索条件も一緒に渡す
    return render_template(
        "borrows/active.html",
        borrows_active_all=borrows_active_all,
        borrows_active=borrows_active_pag,
        today=date.today(),
        page=page,
        total_pages=total_pages,
        search_keyword=search_keyword,
        search_type=search_type,
        form=form
    )
# ===================================================================================================


"""
・削除機能を参考に作成
"""
# 貸出返却処理============================================================================
@borrows.route("/borrows_active_list/<int:id>/return", methods=["POST"])
@login_required
def borrows_return(id):

    # DBから指定されたidの貸出情報を取得（見つからない場合は、404エラー）
    borrow = Borrow.query.get_or_404(id)
    
    # ReturnFormクラスをインスタンス化
    form = ReturnForm()
    
    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        
        # 返却日に今日の日付を登録（更新）
        borrow.returned_at = date.today()
        
        # もし返却日が返却予定日を超えていたらそのユーザーの滞納を１増やす
        if borrow.returned_at > borrow.due_date:
            # Userテーブルから貸出した利用者情報を取得
            user = User.query.get_or_404(borrow.user_id)
            # 滞納を１増やす
            user.overdue_count += 1
            # もし滞納が3以上となれば、ブラックリスト入り
            if user.overdue_count >= 3:
                user.blackflag = True
            # DBの更新
            db.session.add(user)
            db.session.commit()        

        # DBから指定されたid（返却する本のid）の本の情報を取得
        book = Book.query.get_or_404(borrow.book_id)
        # 在庫数を1増やす
        book.stock += 1
        # 本テーブルの内容を更新
        db.session.add(book)
        db.session.commit()
        
        # フラッシュメッセージ
        flash(f"貸出ID：{borrow.borrows_id}が返却されました。")
        
        # 完了したら貸出中の一覧へリダイレクト
        return redirect(url_for("borrows.borrows_active_list"))
    
    # フォームをテンプレートに渡す
    return render_template("borrows/new.html", form=form)
        
# ===================================================================================

"""
・Flask本格入門やさしくわかるWebアプリ開発：P315（CRUD機能：一覧表示）
"""
# 貸出（済）履歴一覧============================================================================
@borrows.route("/borrows_deactive_list")
@login_required
def borrows_deactive_list():
    
    """
    DBテーブル内の値がNONE以外の内容を取り出す方法
    ・https://qiita.com/Bashi50/items/7f2214550e80b87fb922
    """
    # 貸出済（returned_atがNULLでないのもの）のデータを取得。Userの利用者名と、Bookの本のタイトルも取得
    borrows_deactive = db.session.query(
        Borrow,User.name,Book.title
        ).join(
            User,Borrow.user_id == User.user_id
            ).join(
                Book,Borrow.book_id == Book.book_id
                ).filter(Borrow.returned_at != (None)
                         )
                
    """
    検索機能
    ・Python FlaskによるWebアプリ開発入門（教科書） P244～249
    参考サイト
    ・likeを使ったあいまい検索：https://ninja-camp.net/flask/223
    ・request.args.getについて：https://iifx.dev/ja/articles/54724471/%E3%81%93%E3%82%8C%E3%81%A7%E5%AE%8C%E7%92%A7-flask%E3%81%A7%E3%81%AE%E3%82%AF%E3%82%A8%E3%83%AA%E6%96%87%E5%AD%97%E5%88%97%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E5%85%A5%E9%96%80%E3%82%AC%E3%82%A4%E3%83%89
    ・検索テンプレート用１：https://ja.python-3.com/?p=389382
    ・検索テンプレート用２：https://qiita.com/yuuki-h/items/171006db887e0427aae2
    """
    # 検索キーワードを取得
    # GETリクエストのURLパラメータ（?search=xxx）から検索キーワードを取得
    # 第一引数：フォームの <input name="search"> の値を取り出す
    # 第二引数：デフォルト値（空文字）
    # 第三引数：取得した値を文字列型に変換
    # .strip()：検索文字列の無駄な空白を消す
    search_keyword = request.args.get("search", "", type=str).strip()
    
    # ラジオボタンの内容を取得
    # GETリクエストのURLパラメータ（?search_type=xxx）からラジオボタンの選択値を取得
    # 第一引数：フォームの <input name="search_type"> の値を取り出す
    # 第二引数：デフォルト値として「利用者検索（user）」を設定
    # 第三引数：取得した値を文字列型に変換
    search_type = request.args.get("search_type", "user", type=str)
    
    # 検索キーワードが存在する場合（空文字でない場合）にLIKEであいまい検索
    if search_keyword:
        # ラジオボタンの選択が、本のタイトル
        if search_type == "title":
            # 本のタイトルでのあいまい検索（デフォルト）
            borrows_deactive = borrows_deactive.filter(Book.title.like("%" + search_keyword + "%"))
        # ラジオボタンの選択が、利用者名
        else:
            # 利用者名でのあいまい検索
            borrows_deactive = borrows_deactive.filter(User.name.like("%" + search_keyword + "%"))

    # 検索フィルター済みの貸出データの全件取得
    borrows_deactive_all = borrows_deactive.all()

    # ページネーション処理
    borrows_deactive_pag, page, total_pages = pagination(borrows_deactive_all)
    
    # 取得した貸出履歴の情報をテンプレートに渡す
    return render_template("borrows/deactive.html",
                           borrows_deactive_all=borrows_deactive_all,
                           borrows_deactive=borrows_deactive_pag,
                           page=page,
                           total_pages=total_pages,
                            search_keyword=search_keyword,
                            search_type=search_type
                           )
    
# ===================================================================================

"""
・Flask本格入門やさしくわかるWebアプリ開発：P315（CRUD機能：登録）
"""
# 新規貸出の登録==============================================================================
@borrows.route("/borrows_new", methods=["GET", "POST"])
@login_required
def borrows_new():
    
    # Borrowクラスをインスタンス化
    form = BorrowForm()
    
    """
    DBのデータを選択肢としてセットする方法
    ・choicesのセットの仕方１：https://techblog.hys-neko-lab.com/entry/2022/08/06/165940
    ・choicesのセットの仕方２：https://qiita.com/hahirusan/items/b0b940e5ab2f0a68b2db
    """
    # 利用者一覧を取得して選択肢にセット（ブラックリスト者以外をフィルター）
    users = User.query.filter(User.blackflag == False).all()
    # 選択肢として、デフォルトは「選択肢してください」、利用者名を表示
    form.user_id.choices = [(0, "選択してください")] + [(user.user_id, user.name) for user in users]
    
    # 本一覧を取得して選択肢にセット（在庫が0以外をフィルター）
    books = Book.query.filter(Book.stock != 0).all()
    # 選択肢として、デフォルトは「選択肢してください」、本タイトルと在庫数を表示
    form.book_id.choices = [(0, "選択してください")] + [(book.book_id, f"{book.title}：在庫{book.stock}冊") for book in books]
    
    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        
        # formで入力された利用者、本、返却予定日をDBに追加
        borrow = Borrow(
            user_id=form.user_id.data,
            book_id=form.book_id.data,
            due_date=form.due_date.data,
        )
                    
        # DBから指定されたid（貸出される本のid）の本の情報を取得
        book = Book.query.get_or_404(borrow.book_id)
        # DBから指定されたid（貸出される利用者のid）の利用者の情報を取得
        user = User.query.get_or_404(borrow.user_id)
        # DBから指定されたid（貸出される本のid）のジャンルの情報を取得
        bookgenre = BookGenre.query.get_or_404(book.genre_id)
        
        # 在庫数を1減らす
        book.stock -= 1
        # 本の貸出数を増やす
        book.book_borrowed_count += 1
        # 利用者の貸出数を増やす
        user.user_borrowed_count += 1
        # ジャンルの貸出数を増やす
        bookgenre.genre_borrowed_count += 1
        
        # テーブルの内容を更新
        db.session.add(book)
        db.session.add(borrow)
        db.session.add(user)
        db.session.add(bookgenre)
        db.session.commit()
        
        # 完了したら貸出中の一覧へリダイレクト
        return redirect(url_for("borrows.borrows_active_list"))
    
    # フォームをテンプレートに渡す
    return render_template("borrows/new.html", form=form)
# =======================================================================================

# テスト用に作成
# 貸出の削除====================================================================================
@borrows.route("/borrows_list/<int:id>/delete", methods=["POST"])
@login_required
def borrows_delete(id):
    
    # 削除フォームを受け取る
    form = DeleteForm()
    
    # DBから指定されたidの貸出の情報を取得（見つからない場合は、404エラー）
    borrow = Borrow.query.get_or_404(id)
    
    # フォームが送信され、入力内容の検証（バリデーション）が成功した場合
    if form.validate_on_submit():
        # 指定されたidの利用者の情報を削除
        db.session.delete(borrow)
        db.session.commit()
        return redirect(url_for("borrows.borrows_active_list"))
    
    # 完了したらジャンルの一覧へリダイレクト
    return redirect(url_for("borrows.borrows_active_list"))
# ==============================================================================================
