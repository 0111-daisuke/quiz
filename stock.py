import json
import os

# 新しいデータのセット
new_data = {
    "answer": "塵も積もれば山となる",
    "image": "tirimotumoreba.png",
    "candidates": [
        "馬鹿の塵集め",
        "千里の道も一歩から",
        "多くの小さな努力が成功をもたらす"
    ],
    "features": [
        ""
    ]
}

# stockディレクトリのパス
stock_dir = 'stock'

# stockディレクトリが存在しない場合は作成
if not os.path.exists(stock_dir):
    os.makedirs(stock_dir)

# stockディレクトリ内のstock.jsonファイルのパス
stock_json_path = os.path.join(stock_dir, 'stock.json')

# stock.jsonファイルが存在するかチェック
if os.path.exists(stock_json_path):
    # 既存のデータを読み込み
    with open(stock_json_path, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
else:
    # ファイルが存在しない場合、新しいリストを作成
    existing_data = []

# 新しいデータのanswerを取得
new_answer = new_data['answer']

# すでに同じanswerが存在するかチェック
answer_exists = any(item['answer'] == new_answer for item in existing_data)

if not answer_exists:
    # 新しいデータを追加
    existing_data.append(new_data)

    # JSONファイルに保存
    with open(stock_json_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
else:
    print("同じanswerを持つデータが既に存在します。追加しませんでした。")
