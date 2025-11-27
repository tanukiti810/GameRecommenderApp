import os
import time
import requests
from typing import Any
from app.db import games_col  

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
if not RAWG_API_KEY:
    raise RuntimeError("RAWG_API_KEY が環境変数に設定されてないよ")

SWITCH_PLATFORM_ID = 7 

def rawg_fetch_switch_page(page: int, page_size: int = 40, max_retries: int = 3):
    url = "https://api.rawg.io/api/games"

    for attempt in range(1, max_retries + 1):
        try:
            res = requests.get(
                url,
                params={
                    "key": RAWG_API_KEY,
                    "platforms": SWITCH_PLATFORM_ID,
                    "page": page,
                    "page_size": page_size,
                    "ordering": "-added",
                },
                timeout=15,
            )
            res.raise_for_status()
            return res.json()

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else None

            if status is not None and 500 <= status < 600 and attempt < max_retries:
                print(f"page {page}: {status} {e} → {attempt}回目のリトライ中…")
                time.sleep(2 * attempt)
                continue

       
            raise

        except requests.exceptions.RequestException as e:
       
            if attempt < max_retries:
                print(f"page {page}: 接続エラー {e} → {attempt}回目のリトライ中…")
                time.sleep(2 * attempt)
                continue
            raise


    raise RuntimeError(f"page {page}: RAWG に接続できなかった")
def rawg_game_to_doc(game: dict) -> dict:

    raw_genres = game.get("genres") or []
    raw_tags = game.get("tags") or []

    genres_list = [
        g["name"]
        for g in raw_genres
        if isinstance(g, dict) and "name" in g
    ]

    tags_list = [
        t["name"]
        for t in raw_tags
        if isinstance(t, dict) and "name" in t
    ]

    ratings_count = game.get("ratings_count") or 0

    doc = {
        "appid": game["id"],
        "platform_id": game["id"],
        "platform": "switch",

        "name": game.get("name"),
        "genres": [str(genres_list)],
        "tags": [str(tags_list)],
        "categories": [],

        "price": None,
        "release_date": game.get("released"),

        "positive": ratings_count,
        "negative": 0,
    }

    return doc

def import_switch_games(max_pages: int | None = None):
    page = 1
    total = 0
    rawg_total = None

    while True:
        data = rawg_fetch_switch_page(page)
        if rawg_total is None:
            rawg_total = data.get("count")
            print(f"RAWG 上の Switch 該当件数 (count): {rawg_total}")

        results = data.get("results", [])
        if not results:
            print(f"page {page}: 0件 → 終了")
            break

        for game in results:
            try:
                doc = rawg_game_to_doc(game)
            except Exception as e:
                print(f"doc 変換エラー: {e} (id={game.get('id')}, name={game.get('name')}) → この1件はスキップ")
                continue
            
            games_col.update_one(
                {"platform": "switch", "platform_id": doc["platform_id"]},
                {"$set": doc},
                upsert=True,
            )
            total += 1
        print(f"page {page}: {len(results)}件 upsert, 累計 {total}")

     
        if not data.get("next"):
            print("next が無いので終了")
            break

        page += 1

       
        if max_pages is not None and page > max_pages:
            print(f"max_pages={max_pages} 到達 → いったん終了")
            break

        time.sleep(1)

    print("最終 upsert 件数:", total)

if __name__ == "__main__":
    import_switch_games() 
