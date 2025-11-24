from fastapi import FastAPI, Query
from pydantic import BaseModel
from .db import games_col  # MongoDB のコレクション
from typing import Optional, List

app = FastAPI()


# =========================
#  DB → レスポンス用の形に直す関数たち
# =========================

def parse_genres_field(genres_field) -> list[str]:
    """
    DB の genres フィールドをちゃんとしたリストに変換する。

    例:
      genres_field = ["['Action', 'Adventure', 'RPG']"]
      → ["Action", "Adventure", "RPG"]
    """
    if not isinstance(genres_field, list) or not genres_field:
        return []

    first = genres_field[0]  # 今のDBだと文字列が1個だけ入っている
    if not isinstance(first, str):
        return []

    s = first.strip()  # 空白削る

    # 両端の [] を削る
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]

    # カンマ区切りで分ける
    parts = s.split(",")

    result: list[str] = []
    for p in parts:
        p = p.strip()  # 前後の空白を削る

        # 先頭と末尾の ' または " を削る
        if (p.startswith("'") and p.endswith("'")) or (p.startswith('"') and p.endswith('"')):
            if len(p) >= 2:
                p = p[1:-1]

        if p:
            result.append(p)

    return result


# =========================
#  Pydantic モデル
# =========================

class GameBase(BaseModel):
    appid: Optional[int] = None
    name: Optional[str] = None
    platform: Optional[str] = None
    categories: Optional[List[str]] = None
    genre: Optional[List[str]] = None  # ← ここに変換後のジャンルを入れて返す
    negative: Optional[int] = None
    positive: Optional[int] = None
    price: Optional[float] = None
    release_date: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        orm_mode = True
        extra = "ignore"  # _id とかモデルにないフィールドは無視


# =========================
#  ① 全ジャンル一覧 + ジャンル数
# =========================

@app.get("/genres")
def get_genres():
    """
    DB に入ってる genres から、全部のジャンルを集めて
    ・ジャンルの種類数
    ・ジャンル一覧
    を返す。
    """

    # genres フィールドの「中の要素」を distinct で全部取る
    # 今のDBだと "['Action', 'Adventure', 'RPG']" みたいな文字がたくさん返ってくるイメージ
    raw_values = games_col.distinct("genres")

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
        "genre_count": len(genres_sorted),
        "genres": genres_sorted,
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
