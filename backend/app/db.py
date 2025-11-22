import os 
from pymongo import MongoClient

MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL が環境変数に設定されてないよ")

client = MongoClient(MONGO_URL)

# docker-composeで指定したDB名に合わせる
db = client["game_recommender_db"]
games_col = db["steam_games"] #なければ自動で作られる


