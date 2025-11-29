from fastapi import FastAPI, Query
from pydantic import BaseModel
from .db import games_col  # MongoDB のコレクション
from typing import Optional, List

app = FastAPI()


# =========================
#  DB → レスポンス用の形に直す関数たち
# =========================



# =========================
#  ① 全ジャンル一覧 + ジャンル数
# =========================

@app.get("/categories")
def get_categories():
    """
    DB に入ってる genres から、全部のジャンルを集めて
    ・ジャンルの種類数
    ・ジャンル一覧
    を返す。
    """

    # genres フィールドの「中の要素」を distinct で全部取る
    # 今のDBだと "['Action', 'Adventure', 'RPG']" みたいな文字がたくさん返ってくるイメージ
    raw_values = games_col.distinct("categories")

    genre_set: set[str] = set()

    for value in raw_values:
        if not isinstance(value, str):
            continue

        # さっき書いたロジックを再利用したいので、同じようにパース
        # distinct の結果は文字列そのものなので、擬似的に「リスト1個分」として扱う
        temp_list = [value]
        parsed_genres = parse_genres_field(temp_list)

        for g in parsed_genres:
            genre_set.add(g)

    genres_sorted = sorted(genre_set)

    return {
        "categories_count": len(genres_sorted),
        "categories": genres_sorted,
    }


# =========================
#  ② ジャンルを指定してランダム取得
# =========================

@app.get("/games/random", response_model=List[GameBase])
def get_random_games_by_genre(
    genres: List[str] = Query(..., description="抽選に使いたいジャンル（1つ以上）"),
    limit: int = Query(10, ge=1, le=50, description="返す本数（デフォ 10）"),
):
    """
    1. まず DB からランダムに多めにゲームを取る
    2. Python側で genres をパースして、条件に合うやつだけ残す
    """

    # DBからランダムで多めにサンプルを取る
    # limit の 5倍くらい取っといて、その中から条件に合うやつを選ぶ
    pipeline = [
        {"$sample": {"size": limit * 5}}
    ]
    docs = list(games_col.aggregate(pipeline))

    result_docs: list[GameBase] = []

    for doc in docs:
        # Mongo のドキュメントは dict っぽいオブジェクトなので、一旦普通の dict にして触る
        d = dict(doc)

        # _id はそのままだと扱いづらいので一旦消す（レスポンスにいらないし）
        d.pop("_id", None)

        # DB の genres からちゃんとしたリストを作る
        parsed_genres = parse_genres_field(d.get("genres"))
        d["genre"] = parsed_genres  # レスポンス用のフィールドに入れる

        # 指定された genres のどれかが含まれているかチェック
        if genres:
            # genres = ["Action", "RPG"] みたいな時、
            # ゲームの parsed_genres の中にどれか1個でも含まれてたらOK
            if not any(g in parsed_genres for g in genres):
                continue

        # 条件をクリアしたものだけ追加
        result_docs.append(GameBase(**d))

        # limit 個集まったら終了
        if len(result_docs) >= limit:
            break

    return result_docs
