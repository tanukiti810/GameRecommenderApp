from fastapi import FastAPI
from pymongo import MongoClient
import os
import requests

app = FastAPI()
MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL が環境変数に設定されてないよ")
client  = MongoClient(MONGO_URL)
db = client["game_recommender_db"]
games_col = db["steam_games"] #なければ自動で作られる


db.games.create_index("genres")
    

"""
#データベースの中のジャンルを検索する
@app.get("/search_genres/{genre}")
async def search_genres(genre: str):
"""