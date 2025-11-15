# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import time

app = FastAPI()

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

def get_app_info(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=JP&l=english"
    r = requests.get(url)
    data = r.json()
    info = data[str(appid)].get("data", {})
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


appids = [730, 570, 582010]
results = {}
for appid in appids:
    info = get_app_info(appid)
    if info:
        results[appid] = info
        print(f"{info['name']} を保存しました。")
    time.sleep(0.3)

# 保存
with open("steam_app_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("完了！")



