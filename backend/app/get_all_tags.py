import ast
import json
from pathlib import Path
from .db import games_col


def extract_tags(val):
    result = set()
    if val is None:
        return result

    if isinstance(val, dict):
        result.update(val.keys())
        return result

    if isinstance(val, list):
        for item in val:
            result.update(extract_tags(item))
        return result

    if isinstance(val, str):
        s = val.strip()
        try:
            parsed = ast.literal_eval(s)
            result.update(extract_tags(parsed))
        except Exception:
            pass
        return result

    return result


def get_all_tags():
    unique = set()
    cursor = games_col.find(
        {"tags": {"$exists": True, "$ne": []}},
        {"tags": 1}
    )

    for doc in cursor:
        unique.update(extract_tags(doc.get("tags")))

    return sorted(unique)


def main():
    tags = get_all_tags()
    print("ユニークタグ数:", len(tags))
    print("先頭20件:", tags[:20])

    # このファイルと同じフォルダに必ず出す
    out_path = Path(__file__).resolve().parent / "all_tags.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)

    print("保存先:", str(out_path))


if __name__ == "__main__":
    main()
