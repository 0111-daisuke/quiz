import random
import json
import os
# import cv2

file_path = "stock/stock.json"

# JSONファイルを読み込む関数
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# ランダムなデータを取得する関数
def get_random_data():
    data = read_json(file_path)
    random_index = random.randint(0, len(data) - 1)
    return data[random_index]

# ランダムなデータを取得する
def theme():
    random_data = get_random_data()
    
    # 各ステータスを変数に格納
    answer = random_data["answer"]
    image = random_data["image"]
    candidates = random_data["candidates"]
    features = random_data["features"]

    return answer, image, candidates, features

'''
# 画像を開く関数
def open_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
        return

    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: The file '{image_path}' could not be opened.")
        return

    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''

# メイン関数
def main():
    # ランダムなデータを取得
    answer, image, candidates, features = theme()
    print("Answer:", answer)
    print("Image:", image)
    print("Candidates:", candidates)
    print("features:", features)
    
    '''
    # 画像のパスを設定
    image_path = os.path.join("stock", image)

    # 画像を開く
    open_image(image_path)
    '''

# テスト実行
if __name__ == "__main__":
    main()
