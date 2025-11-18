"""
CSV → MongoDB に取り込むスクリプト

・Python 3.10 以降で推奨される構文のみ使用
・非推奨の import は一切使っていない
・初心者でも読めるようにコメント大量
・Docker コンテナ内で動くことを前提にしている

実行方法：
docker compose exec backend python app/import_csv_to_mongo.py
"""

import os            # 環境変数(MONGO_URL)を読むため
import json          # JSON文字列をPythonの型に変換するときに使う
import pandas as pd  # CSV を読み込むライブラリ
from typing import Any
from pymongo import MongoClient


# ============================================================================
# 1. MongoDB に接続する準備
# ============================================================================

# docker-compose.yml に書いた MONGO_URL を読む
MONGO_URL = os.environ.get("MONGO_URL")

# もし設定されてない場合はスクリプトを止める
if not MONGO_URL:
    raise RuntimeError("環境変数 MONGO_URL が設定されていないよ！ docker-compose.yml を確認してね。")

# MongoDB に接続（まだ実際にアクセスはしない「準備だけ」）
client = MongoClient(MONGO_URL)

# 使用するデータベースを指定
db = client["game_recommender_db"]

# この中に保存される
games_col = db["steam_games"]


# ============================================================================
# 2. CSV 内の “配列っぽい文字列” を Python の list に変換する関数
# ============================================================================
def to_list(value: Any) -> list[str]:
    """
    CSV には、
    ・"['Action', 'RPG']"
    ・"Action; RPG"
    ・["Action","RPG"]（JSON 形式）
    など色んな形式で配列が入っている場合がある。

    この関数は「どんな形式でも list[str] に変換して返す」ことだけに集中。
    """

    # まず None は空リスト扱い
    if value is None:
        return []

    # すでに list 型なら文字列化して返す
    if isinstance(value, list):
        return [str(v) for v in value]

    # 文字列として扱う
    text = str(value).strip()

    # 空文字なら空リスト
    if not text:
        return []

    # JSON 形式の可能性がある場合（例："["Action","RPG"]"）
    if text.startswith("[") and text.endswith("]"):
        try:
            parsed = json.loads(text)  # JSON として解釈
            if isinstance(parsed, list):
                return [str(v) for v in parsed]
        except json.JSONDecodeError:
            pass  # ダメなら次の形式へ

    # セミコロン区切り形式（例："Action; RPG"）
    if ";" in text:
        parts = [p.strip() for p in text.split(";") if p.strip()]
        return parts

    # ここまで来たら単なる文字列
    return [text]


# ============================================================================
# 3. メイン処理：CSV を MongoDB に取り込む
# ============================================================================
def import_csv():
    """
    games_march2025_cleaned.csv を読み込んで、
    各ゲームを MongoDB にアップサート（更新 or 新規追加）する。
    """

    print("📁 CSV を読み込んでいます...")

    # CSV ファイルのパス（backend/app/data/ に置く前提）
    csv_path = "app/data/games_march2025_cleaned.csv"

    # pandas で読み込み（UTF-8 でOK）
    df = pd.read_csv(csv_path)

    print(f"📊 {len(df)} 件のゲームデータを読み込みました。")

    # 行ごとに処理
    for _, row in df.iterrows():

        # appid は Steam のユニークID → 絶対にあるはず
        appid = int(row["appid"])

        # 各カラムを安全に取得
        name = str(row.get("name", ""))
        release_date = str(row.get("release_date", ""))
        price = float(row.get("price", 0))

        # リスト系の項目は to_list() で変換
        genres = to_list(row.get("genres"))
        categories = to_list(row.get("categories"))
        tags = to_list(row.get("tags"))

        # レビュー系
        positive = int(row.get("positive", 0))
        negative = int(row.get("negative", 0))

        # ドキュメントとしてまとめる（dict[str, Any]）
        doc: dict[str, Any] = {
            "appid": appid,
            "name": name,
            "release_date": release_date,
            "price": price,
            "genres": genres,
            "categories": categories,
            "tags": tags,
            "positive": positive,
            "negative": negative,
        }

        # MongoDB に upsert（既にあれば更新、なければ新規作成）
        games_col.update_one({"appid": appid}, {"$set": doc}, upsert=True)

    print("取り込み完了！ MongoDB に保存されました。")


# ============================================================================
# 4. スクリプトとして実行された場合だけ動く
# ============================================================================
if __name__ == "__main__":
    import_csv()
