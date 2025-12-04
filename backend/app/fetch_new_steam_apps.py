
import os
import time
import requests
from pymongo import UpdateOne

from .db import db, games_col 

STEAM_API_KEY = os.environ.get("STEAM_API_KEY")
if not STEAM_API_KEY:
    raise RuntimeError("STEAM_API_KEY が環境変数に設定されてないよ")

API_URL = "https://api.steampowered.com/IStoreService/GetAppList/v1/"

def load_existing_appids() -> set[int]:
    existing: set[int] = set()
    for doc in games_col.find({}, {"appid": 1}):
        existing.add(doc["appid"])
    print(f"既存 appid 数: {len(existing)}")
    return existing

def sync_new_appids():
    existing = load_existing_appids()

    last_appid = 0
    total_new = 0

    while True:
        params = {
            "key": STEAM_API_KEY,
            "include_games": "true",
            "include_dlc": "true",
            "include_software": "false",
            "include_videos": "false",
            "include_hardware": "false",
            "max_results": 50000,
            "last_appid": last_appid,
        }

        print(f"request: last_appid={last_appid}")
        resp = requests.get(API_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()["response"]

        apps = data.get("apps", [])
        if not apps:
            print("apps が空だったので終了")
            break

        ops: list[UpdateOne] = []

        for app in apps:
            appid = app["appid"]
            if appid in existing:
                continue  # もう持ってるやつはスキップ

            name = app.get("name", "")

            doc = {
                "appid": appid,
                "name": name,
                "categories": [],
                "genres": [],
                "tags": [],
                "negative": None,
                "positive": None,
                "price": None,
                "release_date": None,
                "platform": "steam",
            }

            ops.append(
                UpdateOne(
                    {"appid": appid},
                    {"$setOnInsert": doc}, 
                    upsert=True,
                )
            )

        if ops:
            result = games_col.bulk_write(ops)
            added = result.upserted_count
            total_new += added
            print(f"今回追加: {added} 件 / 合計追加: {total_new} 件")

        last_appid = data.get("last_appid", 0)
        if not data.get("have_more_results"):
            print("have_more_results = false だったので終了")
            break

        time.sleep(1)

    print(f"最終的な新規追加 appid 数: {total_new}")

if __name__ == "__main__":
    sync_new_appids()
