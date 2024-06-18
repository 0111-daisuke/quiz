import json
import random
from PIL import Image

def open_random_image(n):
    # JSONファイルからデータを読み込む
    with open('stock.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # ランダムに n 番目のデータを選択する
    selected_data = random.choice(data)

    # 選択されたデータのimageフィールドを開く
    image_path = selected_data['image']
    image = Image.open(image_path)
    image.show()

# nを指定してランダムに画像を開く
n = 3  # ここに任意の数値を設定します
open_random_image(n)
