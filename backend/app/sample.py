import json
from pathlib import Path


def search_in_json_files(search_string: str):
    """同じ階層のディレクトリ内のJSONファイルから文字列を検索"""
    current_dir = Path(__file__).parent
    #親のディレクトの取得＝steam_data_collectorのディレクトリ
    search_dir = current_dir.parent
    
    results = []
    
    for json_file in search_dir.rglob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if search_string.lower() in content.lower():
                results.append(str(json_file.relative_to(search_dir)))
        except Exception as e:
            print(f"エラー: {json_file} - {e}")
    
    return results


if __name__ == "__main__":
    search_term = input("検索する文字列を入力してください: ")
    results = search_in_json_files(search_term)
    
    if results:
        print(f"\n見つかったファイル ({len(results)}個):")
        for file in results:
            print(f"  - {file}")
    else:
        print("検索結果が見つかりませんでした。")

    serch_word =input("探したいファイルの文字を選択してください")
    serch_dir  =Path(__file__).parent.parent
    for json_file in serch_dir.rglob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
