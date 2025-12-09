from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
import ast
from bson import ObjectId
from typing import Any,Union,List
from pydantic import BaseModel
from .db import games_col

app = FastAPI()

#サンプル用の保存システム
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Choice(BaseModel):
    selected: List[str] = []
    


@app.post("/api/choose")
def choose_game(data: Choice):
    genres = [g for g in data.selected if g in ALLOWED_GENRES]

    cursor = games_col.find({}).limit(200)

    results = []
    for doc in cursor:
        doc_genres = parse_genres_field(doc.get("genres"))
        if genres and not all(g in doc_genres for g in genres):
            continue

        appid = doc.get("appid")
        name = doc.get("name")

        results.append({
            "appid": appid,
            "name": name,
            "price": doc.get("price", 0),
            "image": f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/header.jpg" if appid else None
        })

    return {"count": len(results), "games": results}

#Reactにデータ返す
@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI!, Githubに変更加えました"}

def parse_genres_field(genres_field) -> List[str]:
    if genres_field is None:
        return []
    if isinstance(genres_field, list):
        if len(genres_field) == 1 and isinstance(genres_field[0], str):
            s = genres_field[0].strip()
            try:
                v = ast.literal_eval(s)
                if isinstance(v, list):
                    return [str(x) for x in v]
            except Exception:
                pass
            return [s]
        return [str(x) for x in genres_field]
    if isinstance(genres_field, str):
        s = genres_field.strip()
        try:
            v = ast.literal_eval(s)
            if isinstance(v, list):
                return [str(x) for x in v]
        except Exception:
            pass
        return [s]
    return []

ALLOWED_GENRES = {"Action","Adventure","RPG","Simulation","Strategy","Sports","Casual"}
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
        "appid": appid,
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
    
# ====== デバッグ用：Mongoに何件入ってるか見るAPI ======
def _convert_id(doc: dict[str, Any]) -> dict[str, Any]:
    d = dict(doc)
    d["_id"] = str(d.get("_id"))
    return d

#クエリを設定している
@app.get("/debug/games")
async def debug_games(limit: int = 100):
    total = games_col.count_documents({})
    cursor = games_col.find({}).limit(limit)
    docs = [_convert_id(doc) for doc in cursor]
    return {"total": total,"sample_limit" : limit, "games": docs}




"""
#とりあえずmainでサーチ用の関数を作る
@app.get("/search/games")
async def search_games(name: str )
"""