import json
import time
from pathlib import Path
from typing import Optional, Tuple

import requests
from .db import games_col

STEAM_APPDETAILS_URL = "https://store.steampowered.com/api/appdetails"

# retry_429 をコンテナ内に保存（volume マウントされてるならホストにも残る）
RETRY_429_PATH = Path(__file__).resolve().parent / "retry_429_appids.json"


class RateLimit429(Exception):
    def __init__(self, appid: int):
        super().__init__(f"429 rate limited for appid={appid}")
        self.appid = appid


def _load_retry_429() -> list[int]:
    if not RETRY_429_PATH.exists():
        return []
    try:
        data = json.loads(RETRY_429_PATH.read_text(encoding="utf-8"))
        return [int(x) for x in data]
    except Exception:
        return []


def _save_retry_429(appids: list[int]) -> None:
    uniq = sorted(set(int(x) for x in appids))
    RETRY_429_PATH.write_text(json.dumps(uniq, ensure_ascii=False, indent=2), encoding="utf-8")


def _add_retry_429(appid: int) -> None:
    appids = _load_retry_429()
    appids.append(int(appid))
    _save_retry_429(appids)


def fetch_price_and_description(appid: int) -> Optional[Tuple[int, str, int, str]]:
    """
    日本ストアの価格(JPY)と説明文(日本語優先)を取得。
    429 のときは RateLimit429 を投げる。
    """
    params = {
        "appids": str(appid),
        "cc": "jp",          # 日本ストア（価格）
        "l": "japanese",     # 日本語（テキスト）
        # filters は外す：短文だけ英語/取りこぼしが起きやすいので安全側
    }

    resp = requests.get(STEAM_APPDETAILS_URL, params=params, timeout=15)

    if resp.status_code == 429:
        raise RateLimit429(appid)

    resp.raise_for_status()

    data = resp.json()
    app_entry = data.get(str(appid))
    if not app_entry or not app_entry.get("success"):
        return None

    data_block = app_entry.get("data")
    if not isinstance(data_block, dict):
        return None

    # --- 価格 ---
    price_info = data_block.get("price_overview")
    if not isinstance(price_info, dict):
        # 無料/販売停止/地域制限など
        return None

    currency = str(price_info.get("currency", ""))
    final_raw = price_info.get("final")
    if final_raw is None:
        return None

    try:
        final_raw_int = int(final_raw)
    except Exception:
        return None

    # Steam はだいたい最小単位(×100)で来るので /100
    price_jpy = final_raw_int // 100

    # 日本円以外は今回いじらない（jp指定でも例外がある）
    if currency != "JPY":
        return None

    # --- 説明文（日本語が無いタイトルは英語になるのは仕様） ---
    desc = (
        data_block.get("short_description")
        or data_block.get("about_the_game")
        or data_block.get("detailed_description")
        or ""
    )

    return price_jpy, currency, final_raw_int, str(desc)


def is_already_done(doc: dict) -> bool:
    """
    「JPY価格が妥当 + description がある」なら完了扱い。
    価格は price_raw//100 と price が一致してるかで判定。
    """
    currency_ok = doc.get("currency") == "JPY"
    price = doc.get("price")
    price_raw = doc.get("price_raw")
    price_ok = (
        currency_ok
        and isinstance(price, (int, float))
        and isinstance(price_raw, int)
        and int(price) == int(price_raw) // 100
    )

    desc = doc.get("description")
    desc_ok = isinstance(desc, str) and len(desc.strip()) > 0

    return price_ok and desc_ok


def update_doc_if_needed(doc: dict, fetched: Tuple[int, str, int, str]) -> bool:
    """
    doc に不足があるところだけ $set する（上書き最小化）。
    戻り値: 更新したら True
    """
    price_jpy, currency, final_raw_int, desc = fetched

    update_doc = {}

    # 価格：すでに正しい JPY が入ってるなら触らない
    cur = doc.get("currency")
    price = doc.get("price")
    price_raw = doc.get("price_raw")
    already_price_ok = (
        cur == "JPY"
        and isinstance(price_raw, int)
        and isinstance(price, (int, float))
        and int(price) == int(price_raw) // 100
    )
    if not already_price_ok:
        update_doc["price"] = int(price_jpy)
        update_doc["currency"] = currency
        update_doc["price_raw"] = int(final_raw_int)

    # description：すでに入ってるなら触らない（上書きしない）
    existing_desc = doc.get("description")
    if not (isinstance(existing_desc, str) and existing_desc.strip()):
        if isinstance(desc, str) and desc.strip():
            update_doc["description"] = desc

    if not update_doc:
        return False

    res = games_col.update_one({"_id": doc["_id"]}, {"$set": update_doc})
    return res.modified_count > 0


def run_all_only_missing(sleep_sec: float = 0.5) -> None:
    """
    全件走査。ただし「すでに完成してるもの」はスキップ。
    429 は retry_429_appids.json に貯める。
    """
    cursor = games_col.find({"platform": "steam"})

    scanned = 0
    updated = 0
    skipped_done = 0
    rate_limited = 0

    for doc in cursor:
        scanned += 1
        appid = doc.get("platform_id") or doc.get("appid")
        if appid is None:
            continue
        appid = int(appid)

        if is_already_done(doc):
            skipped_done += 1
            continue

        try:
            fetched = fetch_price_and_description(appid)
            if fetched is None:
                continue

            if update_doc_if_needed(doc, fetched):
                updated += 1

        except RateLimit429:
            rate_limited += 1
            _add_retry_429(appid)
            print(f"[429] appid={appid} → retry_429 に追加")
            # 429 のときは少し長めに休むと通りやすい
            time.sleep(max(2.0, sleep_sec))

        except Exception as e:
            print(f"[ERROR] appid={appid}: {e}")

        time.sleep(sleep_sec)

    print("\n=== DONE ===")
    print(f"scanned={scanned}, updated={updated}, skipped_done={skipped_done}, 429_saved={rate_limited}")
    print(f"retry file: {RETRY_429_PATH}")


def run_retry_429_only(sleep_sec: float = 1.0) -> None:
    """
    retry_429_appids.json に入ってる appid だけ再実行。
    すでに完成してたらリストから削除。
    """
    appids = _load_retry_429()
    if not appids:
        print("[INFO] retry_429_appids.json が空。やることなし")
        return

    remaining: list[int] = []
    total = len(appids)

    for i, appid in enumerate(appids, start=1):
        print(f"\n=== RETRY ({i}/{total}) appid={appid} ===")

        doc = games_col.find_one({"platform": "steam", "platform_id": appid})
        if not doc:
            doc = games_col.find_one({"platform": "steam", "appid": appid})

        if not doc:
            print("[SKIP] DBに見つからない")
            continue

        if is_already_done(doc):
            print("[OK] すでに完了してるのでリストから除外")
            continue

        try:
            fetched = fetch_price_and_description(appid)
            if fetched is None:
                print("[SKIP] 取得できなかった（無料/制限/データなし等）→ 残す")
                remaining.append(appid)
            else:
                changed = update_doc_if_needed(doc, fetched)
                print(f"[OK] 更新: {changed}")
                # 更新できた/できなくても、次回に残すかは「まだ未完了か」で判断
                doc2 = games_col.find_one({"_id": doc["_id"]})
                if doc2 and not is_already_done(doc2):
                    remaining.append(appid)

        except RateLimit429:
            print("[429] まだレート制限 → 残す")
            remaining.append(appid)
            time.sleep(max(3.0, sleep_sec))

        except Exception as e:
            print(f"[ERROR] appid={appid}: {e}")
            remaining.append(appid)

        time.sleep(sleep_sec)

    _save_retry_429(remaining)
    print(f"\n[INFO] retry_429 残り: {len(remaining)} 件")
    print(f"retry file: {RETRY_429_PATH}")


if __name__ == "__main__":
    import sys

    if "--retry-429" in sys.argv:
        run_retry_429_only()
    else:
        run_all_only_missing()
