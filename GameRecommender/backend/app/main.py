from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
import os
from bson import ObjectId

from pymongo import MongoClient

app = FastAPI()

#サンプル用の保存システム
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI!, Githubに変更加えました"}

#=====================MongoDB接続設定=====================
MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL が環境変数に設定されてないよ")

client = MongoClient(MONGO_URL)

# docker-composeで指定したDB名に合わせる
db = client["game_recommender_db"]
games_col = db["steam_games"] #なければ自動で作られる


# ===========Steam から1ゲーム分の情報をとる関数===========
def get_app_info(appid: int):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=JP&l=english"
    r = requests.get(url,timeout = 10)
    data = r.json()
    
    app_data = data.get(str(appid))
    if not app_data or not app_data.get("success"):
        return None
    
    info = app_data.get("data",{})
    if not info or info.get("type") != "game":
        return None

    result = {
        "name": info.get("name"),
        "genres": [g["description"] for g in info.get("genres", [])],
        "categories": [c["description"] for c in info.get("categories", [])],
        "price": info.get("price_overview", {}).get("final", 0) / 100,
        "discount_percent": info.get("price_overview", {}).get("discount_percent", 0),
        "release_date": info.get("release_date", {}).get("date"),
        "metacritic_score": info.get("metacritic", {}).get("score"),
        "is_free": info.get("is_free", False)
    }
    return result


# =========== テストで3本だけmongoに保存する処理 ===========
def save_sample_games_to_mongo():
    
    appids = [730, 570, 582010]
    for appid in appids:
        info = get_app_info(appid)
        if not info:
            print(f"appid {appid}はゲーム情報が取れなかった")
            continue
        
        # appid をキーにupsert
        games_col.update_one(
            {"appid": appid},
            {"$set":info},
            upsert=True
        )
        
        print(f"{info['name']} MongoDBに保存しました")
        time.sleep(0.3)
    print("保存完了！")
    
# uvicorn で起動するときはここは実行されない
# [データ突っ込みたいときだけ] pythonで直接やる
if __name__ == "__main__":
    save_sample_games_to_mongo()


def convert_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/debug/games")
async def debug_games():
    count = games_col.count_documents({})
    docs = list(games_col.find().limit(5))
    docs = [convert_id(d) for d in docs]

    return {
        "count": count,
        "sample": docs,
    }