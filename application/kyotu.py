"""
ページネーションの作り方
・https://ninja-camp.net/flask/224
"""

# ページネーション用
from flask_paginate import Pagination, get_page_parameter
from flask import request


# ページネーション関数：関数化して一覧関係を全てページネーション付ける====================
def pagination(db):

    # 現在のページ番号を取得（指定がなければ1ページ目）
    page = request.args.get("page", default=1, type=int)

    # 1ページあたりに表示する件数(10件)
    per_page = 10

    # データの総件数
    total = len(db)

    # 総ページ数を計算（切り上げ）
    # 25件なら、 25 / 10 = 2.5で3ページ
    total_pages = (total + per_page - 1) // per_page

    # 1未満なら1ページ目に強制
    if page < 1:
        page = 1
    # 総ページ数を超えていたら最終ページへ
    if total_pages > 0 and page > total_pages:
        page = total_pages

    # 開始位置と終了位置を計算
    # 2ページ目なら start=10, end=20
    start = (page - 1) * per_page
    end = start + per_page

    # 現在のページに表示するデータ
    db_list = db[start:end]
    
    # db_list：現在のページに表示するデータ
    # page：現在のページ番号
    # total_pages：総ページ数
    return db_list, page, total_pages
# ==================================================================================