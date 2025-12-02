from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
from bson import ObjectId
from typing import Any,List,Optional,Union
from pydantic import BaseModel
from .db import games_col

app = FastAPI()

#コミット用

#ジャンルの
def parse_genres_field(genres_field) -> list[str]:


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
    genre: Optional[List[str]] = None  
    negative: Optional[int] = None
    positive: Optional[int] = None
    price: Optional[float] = None
    release_date: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        orm_mode = True
        extra = "ignore"  # _id とかモデルにないフィールドは無視




#サンプル用の保存システム
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Choice(BaseModel):
    selected: Union[str,List[str]]
#二十定義になるのでいったん削除
"""
@app.post("/api/choose")
def choose_game(data: Choice):
    print("受け取ったデータ:", data.selected)
    return {"status": "ok", "received": data.selected}
"""
#Reactからデータ受け取り
@app.post("/api/choose",response_model=List[GameBase])
def choose_game(data: Choice):
    if isinstance(data.selected,list):
        genres = data.selected
    else:
        genres = [data.selected]
    limit = 5
    pipeline = [
        {"$sample":{"size": limit * 5}}
    ]
    docs = list(games_col.aggregate(pipeline))
    result_docs: list[GameBase] = []
    for doc in docs:
        d = dict(doc)
        d.pop("_id",None)
        parsed_genres = parse_genres_field(d.get("genres"))
        d["genre"] = parsed_genres

        if not all (g in parsed_genres for g in genres):
            continue

        result_docs.append(GameBase(**d))

        if len(result_docs)>=limit:
            break
    return result_docs

#Reactにデータ返す
@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI!, Githubに変更加えました"}

@app.get("/api/games")
def get_games():
    return [
        {
            "id": 730,
            "title": "CounterStrike 2",
            "description": "20年以上にわたり、Couter-Strikeは世界中の何百万人ものプレイヤーに、最高の対戦エクスペリエンスを提供してきました。そして今、CSの次なるチャプターが幕を開けようとしています。それが『Counter-Strike 2』です。",
            "image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/730/header.jpg?t=1749053861",
            "price": 0
        },
        {
            "id": 2799860,
            "title": "イナズマイレブン 英雄たちのヴィクトリーロード",
            "description": "収集・育成サッカーRPG「イナズマイレブン」シリーズ最新作。 新主人公が活躍する新たな物語、5,400人を超える歴代選手の収集・育成、オンラインの全国大会などが楽しめる。",
            "image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2799860/d0e8ff66995b0cc3baf4d8a439fbfb1e57583c2c/header_japanese.jpg?t=1764296831",
            "price": 8910
        },
    ]



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




# uvicornで起動したときはここは動かない
# 「データ突っ込みたいときだけ」コンテナ内で python app/main.py を叩く
if __name__ == "__main__":
    save_sample_games_to_mongo()
#この部分はファイルごとコミットしないとビルドしないということ

"""
#とりあえずmainでサーチ用の関数を作る
@app.get("/search/games")
async def search_games(name: str )
"""