"""
steam.py

やってることの全体像：

1. Steam の公式 API から「全アプリ一覧（GetAppList）」を取る
2. 各 appid ごとに「appdetails」API を叩いてゲームの詳細情報を取る
3. その中から「type == 'game'」だけを選んで
4. MongoDB に 1件ずつ保存（存在する場合は更新、なければ新規追加）

※ このファイルは「バックエンド用バッチスクリプト」という位置づけ。
   普段は FastAPI が動いてて、
   データをまとめて入れたいときだけ
   `docker compose exec backend python app/steam.py`
   みたいに叩いて使うイメージ。
"""

import os      # OS（環境変数など）にアクセスするための標準ライブラリ
import time    # スリープ(待ち時間)を入れるための標準ライブラリ
import json    # JSON文字列 ⇔ Pythonのdict に変換するライブラリ

import requests          # HTTPリクエスト(外部APIを叩く)用ライブラリ
from tqdm import tqdm    # 進捗バー表示用ライブラリ
from pymongo import MongoClient  # MongoDB に接続するためのライブラリ


# ==============================
# MongoDB に接続する
# ==============================

# docker-compose.yml の backend サービスに書いてある環境変数を読む
#   environment:
#     - MONGO_URL=mongodb://mongo:27017/game_recommender_db
#
# os.environ は「環境変数が入っている辞書」だと思えばOK
MONGO_URL = os.environ.get("MONGO_URL")

# MONGO_URL が設定されてなかったら、このスクリプトは動かせないので強制終了
if not MONGO_URL:
    raise RuntimeError("MONGO_URL が環境変数に設定されてないよ（docker-compose.yml を確認して）")

# MongoDB クライアントを作成
# ここでまだ実際に接続チェックはされず、「接続する準備完了」くらいのイメージ
client = MongoClient(MONGO_URL)

# 接続先 DB を指定
# docker-compose で指定している DB 名: game_recommender_db
db = client["game_recommender_db"]

# 使用するコレクション（テーブルっぽいもの）を指定
# 存在しなくても、初めて insert したタイミングで自動で作られる
games_col = db["steam_games"]


# ==============================
# メインの処理
# ==============================

def fetch_and_save_games(limit: int | None = 1000):
    """
    Steam の API からゲーム情報を取得して、MongoDB に保存する。

    :param limit: 何件まで処理するかの上限。
                  None を渡すと「全件やる」。
                  テスト中は 1000 件など、小さい数字にしておくと安全。
    """

    # --- 1. 全アプリ一覧(GetAppList) を取得する ---

    # Steam の全アプリ一覧を返す公式 API
    # ここでは "applist" の中に "apps": [ {appid, name}, ... ] が入ってくる
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

    # timeout=20 は「20秒待っても返事が来なかったら諦める」という意味
    res = requests.get(url, timeout=20)
    
    print("DEBUG status:", res.status_code)
    print("DEBUG url:", res.url)
    print("DEBUG body head:", res.text[:300])  # 先頭300文字だけ表示


    # HTTPステータスコード(404, 500など)がエラー系だったら例外を投げる
    # → ここでエラーになったら try/except していないので、そのままクラッシュしてOK
    res.raise_for_status()

    # JSON 文字列 → Python の dict に変換
    data = res.json()

    # data の構造: {"applist": {"apps": [ { "appid": 10, "name": "GameName" }, ... ]}}
    apps = data["applist"]["apps"]

    # limit が指定されていたらその件数だけに絞る（テスト用）
    if limit is not None:
        apps = apps[:limit]

    # tqdm(...) で for ループに進捗バーがつく
    for app in tqdm(apps, desc="Fetching game details"):
        # app は {"appid": 10, "name": "GameName"} みたいな dict
        appid = app["appid"]

        # --- 2. 各 appid について appdetails API を叩く ---

        # ストアページから詳細データを返してくれる API
        # cc=JP : 日本のストア情報
        # l=english : 説明文等は英語
        #   ※日本語がよければ "japanese" に変更してもOK
        detail_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=JP&l=english"

        try:
            # 1本のゲームの詳細情報を取得
            detail_res = requests.get(detail_url, timeout=10)
            # HTTPエラーがあれば例外を投げる
            detail_res.raise_for_status()

            # JSON をパース
            # たまに壊れたJSONが返ってきたりするので try/except しておく
            try:
                detail_data = detail_res.json()
            except json.JSONDecodeError:
                print(f"{appid} のJSONデコードに失敗しました")
                continue

            # 通常、この API のレスポンスは { "appid文字列": { ... } } という形
            # 例: { "570": { "success": true, "data": {...} } }
            if not isinstance(detail_data, dict):
                print(f"{appid}: detail_data が dict じゃない ({type(detail_data)})")
                continue

            # appid は int なので、キーとして使うときは str(appid) にする
            app_detail = detail_data.get(str(appid))

            # app_detail が存在しない or 変な型の場合はスキップ
            if not app_detail or not isinstance(app_detail, dict):
                print(f"{appid}: app_detail が存在しないか不正")
                continue

            # app_detail["success"] が False の場合、そのゲームは無効 or 削除済み
            if not app_detail.get("success", False):
                print(f"AppID {appid} 無効または削除済み")
                continue

            # 実際のゲーム情報は "data" キーに入っている
            app_data = app_detail.get("data", {})
            if not isinstance(app_data, dict):
                print(f"{appid}: app_data が不正")
                continue

        # ネットワークエラー全般(Exception) + JSONエラー をまとめてキャッチ
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"{appid} の取得に失敗しました: {e}")
            continue

        # --- 3. "game" タイプだけを抽出 ---

        # type には "game", "dlc", "demo", "tool" などがあるので、
        # ゲーム以外はスキップ
        if app_data.get("type") != "game":
            continue

        # --- 4. MongoDBに保存するためのドキュメントを整形 ---

        # ジャンルは配列で入っているので、
        # [{"id": 1, "description": "Action"}, ...]
        # から "Action" だけを取り出して ["Action", ...] にする
        genres = [g["description"] for g in app_data.get("genres", [])]

        # 必要最低限の情報だけ詰めておく
        # あとで欲しい項目（価格・タグ・プラットフォームなど）が出てきたら
        # ここに増やしていけばOK
        doc = {
            "appid": appid,
            "name": app_data.get("name"),
            "genres": genres,
        }

        # --- 5. MongoDB に upsert（更新 or 新規追加） ---

        # update_one(filter, update, upsert=True)
        #   filter: {"appid": appid} → このappidのドキュメントを探す
        #   update: {"$set": doc} → docの内容でフィールドを上書き
        #   upsert=True → もし見つからなければ新規作成
        games_col.update_one(
            {"appid": appid},
            {"$set": doc},
            upsert=True,
        )

        # API 連打しすぎると先方に負担をかけるので、
        # 優しさとして 0.1秒だけ休ませる
        time.sleep(0.1)

    print("取得＆保存 完了！")


# このブロックの意味：
#
#   ・Pythonファイルは2パターンの使われ方がある
#       1. スクリプトとして直接実行 → `python steam.py`
#       2. 他のファイルから import される → `import steam`
#
#   ・if __name__ == "__main__": は
#      「直接実行されたときだけこの中を動かす」
#      というおまじない。
#
#   ・今回の用途だと `docker compose exec backend python app/steam.py`
#     のように「直接実行」するので、ここが動く。
if __name__ == "__main__":
    # とりあえずテスト中は 1000件だけ
    # 本気で全件取りたいときは None にする（ただし時間はかなりかかる）
    fetch_and_save_games(limit=1000)
