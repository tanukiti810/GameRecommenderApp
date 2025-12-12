from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
import ast
from bson import ObjectId
from typing import Any,Union,List,Literal,Dict
from pydantic import BaseModel
from .db import games_col
import os 

app = FastAPI()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Sidebar のタグID -> Steamの tags_list の文字列
TAG_ALIAS: dict[str, str] = {
    # ---- アクション系 ----
    "FPS": "FPS",
    "ThirdPersonShooter": "Third-Person Shooter",
    "HackAndSlash": "Hack and Slash",
    "Platformer": "Platformer",
    "BulletHell": "Bullet Hell",
    "Metroidvania": "Metroidvania",
    "SoulsLike": "Souls-like",
    "RogueLite": "Rogue-lite",
    "Roguelike": "Rogue-like",

    # ---- アドベンチャー系 ----
    "Exploration": "Exploration",
    "WalkingSimulator": "Walking Simulator",
    "VisualNovel": "Visual Novel",
    "ChoicesMatter": "Choices Matter",
    "Mystery": "Mystery",
    "Horror": "Horror",
    "SurvivalHorror": "Survival Horror",

    # 必要になったらここに増やしていけばOK
}

ALL_TAGS: set[str] = {
    "4X",
    "ARPG",
    "AlternateHistory",
    "Ancient",
    "Anime",
    "AutoBattler",
    "Baseball",
    "Basketball",
    "BattleRoyale",
    "Boxing",
    "Builder",
    "Building",
    "BulletHell",
    "CRPG",
    "CardBattler",
    "ChoicesMatter",
    "Clicker",
    "Coop",
    "Cozy",
    "Crafting",
    "Cyberpunk",
    "Drama",
    "DungeonCrawler",
    "Emotional",
    "Exploration",
    "FPS",
    "Fantasy",
    "FarmingSim",
    "Fighting",
    "Fishing",
    "Flight",
    "Golf",
    "GrandStrategy",
    "HackAndSlash",
    "HandDrawn",
    "Horror",
    "JRPG",
    "LifeSim",
    "LocalCoop",
    "LoreRich",
    "LowPoly",
    "MMORPG",
    "MOBA",
    "Management",
    "Match3",
    "Medieval",
    "Metroidvania",
    "Moddable",
    "Mystery",
    "Mythology",
    "OnlineCoop",
    "PixelGraphics",
    "Platformer",
    "Puzzle",
    "PvE",
    "PvP",
    "RTS",
    "Racing",
    "Relaxing",
    "RogueLite",
    "Roguelike",
    "RoguelikeDeckbuilder",
    "Sandbox",
    "SciFi",
    "Soccer",
    "SoulsLike",
    "SpaceSim",
    "StoryRich",
    "Stylized",
    "Supernatural",
    "SurvivalHorror",
    "TBS",
    "ThirdPersonShooter",
    "TowerDefense",
    "TurnBased",
    "VehicleSim",
    "VisualNovel",
    "WalkingSimulator",
    "WorldWar",
}

ALLOWED_GENRES = {
    "Action",
    "Adventure",
    "RPG",
    "Simulation",
    "Strategy",
    "Sports",
    "Casual",
}

#サンプル用の保存システム
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Choice(BaseModel):
    genres: List[str] = []
    tags: List[str]= []
    limit: int = 200
    
class ChatHistoryItem(BaseModel):
    # "user" か "assistant" か
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    # 今回送るメッセージ本体
    message: str
    # それまでの会話履歴
    history: list[ChatHistoryItem] = []


class ChatResponse(BaseModel):
    # AI の返答文
    reply: str


@app.post("/api/choose")
def choose_game(data: Choice):
    # 1) リクエストを整形
    genres = data.genres or []
    raw_tags = data.tags or []
    limit = data.limit

    # フロントのタグID -> Steamタグ文字列
    normalized_tags = [TAG_ALIAS.get(t, t) for t in raw_tags]

    print("受け取った genres:", genres)
    print("受け取った tags:", raw_tags, " => ", normalized_tags)

    # 2) MongoDB のクエリを組み立て
    query: Dict[str, Any] = {
        "platform": "steam",
    }

    # 親ジャンルは OR 条件（どれか1つ含んでいればOK）
    if genres:
        query["genres_list"] = {"$in": genres}

    # タグは AND 条件（全部含んでるゲームだけ）
    if normalized_tags:
        query["tags_list"] = {"$in": normalized_tags}

    # 3) 実際に検索
    cursor = games_col.find(query).limit(limit)

    games: list[dict[str, Any]] = []
    for doc in cursor:
        appid = doc.get("appid")
        if not appid:
            continue

        name = doc.get("name", "")
        price = float(doc.get("price") or 0)
        description = (
            doc.get("short_description")
            or doc.get("description")
            or ""
        )
        image = (
            f"https://shared.akamai.steamstatic.com/store_item_assets/"
            f"steam/apps/{appid}/header.jpg"
        )

        games.append(
            {
                "appid": appid,
                "name": name,
                "price": price,
                "image": image,
                "short_description": description,
            }
        )

    return {"count": len(games), "games": games}

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

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(body: ChatRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY が設定されてないよ")

    messages = [
        {
            "role": "system",
            "content": "日本語でカジュアルに答えてください。"
        }
    ]
    for h in body.history:
        messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": body.message})

    resp = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-5-mini",
            "messages": messages,
        },
        timeout=30,
    )

    if resp.status_code != 200:
        print("OpenAI error:", resp.status_code, resp.text)
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI error {resp.status_code}: {resp.text}"
        )

    data = resp.json()
    reply_text = data["choices"][0]["message"]["content"]
    return ChatResponse(reply=reply_text)


"""
#とりあえずmainでサーチ用の関数を作る
@app.get("/search/games")
async def search_games(name: str )
"""