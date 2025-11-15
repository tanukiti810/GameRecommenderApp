import requests
import json
from tqdm import tqdm
import  concurrent.futures

# APIのURL（実際のものを入れてください）

try:

    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/" 
    all_games = []
    res = requests.get(url, timeout=10)
    res.raise_for_status()

    data = res.json()

    for app in tqdm(data["applist"]["apps"][:1000], desc="Fetching game details"):
        appid = app["appid"]
        detail_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=JP&l=english"
       
        try:
            detail_res = requests.get(detail_url, timeout=10)
            
            try:
                detail_data = detail_res.json()
            except json.JSONDecodeError:
                print(f"{appid}のJSONデコードに失敗しました")
                continue
           
            if not isinstance(detail_data,dict):
                print(f"{appid}: detail_dataが不正({type(detail_data)})")
                continue

            app_detail = detail_data.get(str(appid))
            if not app_detail or not isinstance(app_detail, dict):
                print(f"{appid}: app_detailが存在しないか不正")
                continue

            if not app_detail.get("success", False):
                print(f"AppID {appid} 無効または削除済み")
                continue

            app_data = app_detail.get("data", {})
            if not isinstance(app_data, dict):
                print(f"{appid}: app_dataが不正")
                continue

        except  (requests.exceptions.RequestException, json.JSONDecodeError):
            print(f"{appid}の取得に失敗しました")
            continue

        

        if app_data.get("type") != "game":
            continue

        all_games.append({
            "appid": appid,
            "name": app_data.get("name"),
            "genres": [g["description"] for g in app_data.get("genres", [])]
        })



    with open("all_apps_raw.json", "w", encoding="utf-8") as f:
        json.dump(all_games, f, ensure_ascii=False, indent=2)
    

except KeyError as e:
    print(f" 想定外のJSON構造: {e}")
except requests.exceptions.RequestException as e:
    print(f" HTTPエラー: {e}")
except ValueError:
    print(" JSONパース失敗（レスポンスがJSONでない可能性）")


#import requests
#import json

#sample_game_data = 340

#all_data_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
#all_data_info =f"https://store.steampowered.com/api/appdetails?appids={sample_game_data}&cc=JP&l=english"
#response =requests.get(all_data_info)
###response.raise_for_status()
#data = response.json()

#app_count = len(data["applist"]["apps"])

#def fetch_url(url):
    
#for num in all_data_url:
    