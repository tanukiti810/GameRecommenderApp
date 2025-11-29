import os
from pymongo import MongoClient
from .db import games_col



collection_name = games_col.find(
    {platform:"steam"},
    {appid:1,id:0}
)

appids = [doc[id]for doc in collection_name if appid in doc]


if __name__ == "__main__":
    tag_all_as_steam()
    check_connection()