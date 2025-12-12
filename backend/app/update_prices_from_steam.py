
import time
from typing import Optional, Tuple

import requests
from bson import ObjectId
from .db import games_col

STEAM_APPDETAILS_URL = "https://store.steampowered.com/api/appdetails"


def fetch_price_and_description(
    appid: int,
) -> Optional[Tuple[int, str, int, str]]:

    params = {
        "appids": str(appid),
        "cc": "jp",  # 日本ストア
        "filters": "price_overview,description",
    }

    try:
        resp = requests.get(STEAM_APPDETAILS_URL, params=params, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERROR] appid={appid} へのリクエストに失敗: {e}")
        return None

    data = resp.json()
    app_entry = data.get(str(appid))
    if not app_entry or not app_entry.get("success"):
        print(f"[SKIP] appid={appid}: success=False or data なし")
        return None

    data_block = app_entry.get("data", {})

    if not isinstance(data_block,dict):
        print(f"[SKIP]appid={appid}: unexpected data type {type(data_block)}")
        return None

    price_info = data_block.get("price_overview")
    if not price_info:
        # 無料ゲームとか価格情報がないもの
        print(f"[SKIP] appid={appid}: price_overview なし（無料や非販売など）")
        return None

    currency: str = price_info.get("currency", "")
    final_raw = price_info.get("final")
    if final_raw is None:
        print(f"[SKIP] appid={appid}: final なし")
        return None

    price_jpy = int(round(final_raw / 100))

    # --- 説明文 ---
    short_desc: str = data_block.get("short_description") or ""


    return price_jpy, currency, int(final_raw), short_desc


def update_all_prices_and_descriptions(sleep_sec: float = 0.5) -> None:

    cursor = games_col.find({"platform": "steam"})

    total = 0
    updated = 0

    for doc in cursor:
        total += 1
        doc_id = doc.get("_id")
        appid = doc.get("appid") or doc.get("platform_id")

        if not isinstance(appid, (int, float, str)):
            print(f"[SKIP] _id={doc_id}: appid 不正 {appid!r}")
            continue

        appid_int = int(appid)

        print(f"\n=== appid={appid_int} | name={doc.get('name')} ===")
        before_price = doc.get("price")

        result = fetch_price_and_description(appid_int)
        if result is None:
            continue

        price_jpy, currency, final_raw, short_desc = result

        update_doc = {
            "price": price_jpy,             # JPY で上書き
            "currency": currency,           # "JPY"
            "price_raw": final_raw,         # Steam の生の値
        }

        if short_desc:
            # main.py は short_description を優先して description を fallback に使ってるので、
            # ここでは両方同じ値を入れておく。
            update_doc["short_description"] = short_desc
            update_doc["description"] = short_desc

        res = games_col.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": update_doc},
        )

        if res.modified_count:
            updated += 1

        print(
            f"[UPDATED] appid={appid_int}: price {before_price} -> {price_jpy} ({currency}), "
            f"short_description set={bool(short_desc)}, "
            f"matched={res.matched_count}, modified={res.modified_count}"
        )

        # API 叩きすぎ防止（適当に調整してOK）
        time.sleep(sleep_sec)

    print("\n=== DONE ===")
    print(f"total scanned:  {total}")
    print(f"total updated:  {updated}")


if __name__ == "__main__":
    update_all_prices_and_descriptions()
