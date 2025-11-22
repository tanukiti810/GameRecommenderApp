from .db import games_col
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
    
    
def check_connection():
    # Atlasに本当に繋がってるか確認
    try:
        client.admin.command("ping")
        host = MONGO_URL.split("@")[-1].split("/")[0]
        print(" MongoDB に接続できたっぽい host:", host)
    except Exception as e:
        print(" 接続エラー:", repr(e))
        return

    total = games_col.count_documents({})
    print("steam_games の件数:", total)

    sample = games_col.find_one({}, {"_id": 0, "name": 1, "appid": 1})
    print("サンプルドキュメント1件:", sample)

if __name__ == "__main__":
    tag_all_as_steam()
    check_connection()