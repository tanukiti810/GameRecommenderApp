import os
from pymongo import MongoClient
MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    raise RuntimeError("MONGO_URL が環境変数に設定されてないよ")
client = MongoClient(MONGO_URL)
db = client["game_recommender_db"]
games_col = db["steam_games"] #なければ自動で作られる

def tag_all_as_steam():
    result = games_col.update_many(
        {},
        {
            "$set": {"platform": "steam",
            },
        "$setOnInsert":{},
        },
    )

    # appid を使って platform_id を埋める（appid があるものだけ）
    result2 = games_col.update_many(
        {"appid": {"$exists": True}},
        [
            {
                "$set": {
                    "platform_id": "$appid"
                }
            }
        ]
    )

    print("platform を steam に設定した件数:", result.modified_count)
    print("platform_id を appid からコピーした件数:", result2.modified_count)

if __name__ == "__main__":
    tag_all_as_steam()