import ast
from .db import games_col


def extract_tag_keys(tags_field):
    """tags フィールドからタグ名だけのリストを作る"""
    if not tags_field:
        return []

    # 例: ["{'Mythology': 9421, 'Action RPG': 7720, ...}"]
    if isinstance(tags_field, list) and len(tags_field) > 0 and isinstance(tags_field[0], str):
        s = tags_field[0]
        try:
            d = ast.literal_eval(s)
            if isinstance(d, dict):
                return list(d.keys())
        except Exception:
            return []
        return []

    # 例: {"Mythology": 9421, "Action RPG": 7720}
    if isinstance(tags_field, dict):
        return list(tags_field.keys())

    # 例: "{'Mythology': 9421, ...}" 1個だけ
    if isinstance(tags_field, str):
        try:
            d = ast.literal_eval(tags_field)
            if isinstance(d, dict):
                return list(d.keys())
        except Exception:
            return []
        return [tags_field]

    return []


def extract_genres_list(genres_field):
    """genres フィールドからジャンル名のリストを作る"""
    if not genres_field:
        return []

    # 例: ["['Action', 'Adventure', 'RPG']"]
    if isinstance(genres_field, list) and len(genres_field) == 1 and isinstance(
        genres_field[0], str
    ):
        s = genres_field[0]
        try:
            v = ast.literal_eval(s)
            if isinstance(v, list):
                return [str(x) for x in v]
        except Exception:
            return []
        return []

    # すでに ["Action", "Adventure"] 形式
    if isinstance(genres_field, list):
        return [str(x) for x in genres_field]

    if isinstance(genres_field, str):
        return [genres_field]

    return []


def main(batch_size: int = 1000):
    """
    tags_list / genres_list が無いドキュメントを
    _id 昇順で batch_size 件ずつ処理する。
    CursorNotFound を避けるために、カーソルはバッチごとに作り直す。
    """

    last_id = None
    total = 0

    while True:
        query = {"tags_list": {"$exists": False}}
        if last_id is not None:
            query["_id"] = {"$gt": last_id}

        # ★ ここがポイント：毎ループでカーソルを作り直し＋limit
        docs = list(
            games_col.find(query, {"tags": 1, "genres": 1})
            .sort("_id", 1)
            .limit(batch_size)
        )

        if not docs:
            break  # 処理対象がもう無い

        for doc in docs:
            last_id = doc["_id"]

            tags_list = extract_tag_keys(doc.get("tags"))
            genres_list = extract_genres_list(doc.get("genres"))

            update = {}
            update["tags_list"] = tags_list
            update["genres_list"] = genres_list

            games_col.update_one({"_id": doc["_id"]}, {"$set": update})
            total += 1

        print(f"processed {total} docs so far, last_id={last_id}")

    print("done. total processed:", total)


if __name__ == "__main__":
    main()
