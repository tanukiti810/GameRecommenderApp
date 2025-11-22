from fastapi import FastAPI
import requests
from fastapi import Query
from .db import games_col

app = FastAPI()



#検索用のデータ
class GameBase[BaseModel]:
    platform : str | None = None
    categories: list[str] | None = None
    genre: list[str] | None = None
    metacritic_score: int | None = None
    prise: float | None= None
    release_date: str | None = None
    negative : int | None = None
    positive : int | None = None
    tags : list [str] | None = None
     


db.games.create_index("genres")
    

#データベースの中のジャンルを検索する
#大量の引数を設定する、要素がなくてもエラーにならないようにしている
@app.get("/games/search",response_model = list[GameBase])
def search_games(
    genres : list[str] | None = Query(default = None, description ="複数のジャンルを選択可能"),
    price_min : float | None =  Query(default = None, description = "最低価格" ),
    price_max : float | None = Query(default = None, description = "最高価格"),
    score_min : int | None = Query(default = None, description= "最低メタスコア"),
    positive_min : int | None = Query(default = None, description = "一番引くい評価された数" ),
    limit : int = Query (default = 5, ge = 1, le=10, description = "取得件数の上限"),
):
    mongo_filter: dict = {}
    
    if genres:
        mongo_filter["genre"] = {"$in": genres}
    if price_min is not None or price_max is not None:
        price_dic: dict = {}
        if price_min is not None:
            price_dic["$gte"] = price_min
        if price_max is not None:
            price_dic["$lte"] = price_max
        mongo_filter["price"] = price_dic
    
