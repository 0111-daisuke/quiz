from openai import OpenAI
import requests
import os
import json

client = OpenAI()

answer = input("ことわざを入力: ")

# 単語生成用の設定
def word_create_api(messages):
    return client.chat.completions.create(
        model = "gpt-4o",
        messages = messages,
        temperature = 1.0,
        max_tokens = 100
        )

# 画像生成用の設定
def generate_image_api(prompt):
    return client.images.generate(
        model = "dall-e-3",
        prompt = prompt,
        size = "1024x1024",
        quality = "standard",
        n = 1
        )

# 単語生成
def generate_words():
    
    # hostのプロンプト
    words_create_messages = [
        {"role": "system",
         "content": f"""
         以下の例を参考にことわざ{answer}から連想される単語を4個出してください。
         【例】
         ことわざ: 犬も歩けば棒に当たる
         犬、棒、失敗、災難
         """}
        ]
    
    response = word_create_api(words_create_messages)
    words_list = response.choices[0].message.content

    words_combined = ' '.join(words_list)

    return words_combined

# 画像を生成する関数
def generate_image(words):
    prompt = f"""
              以下の要素を含めた画像を生成してください。画像には以下の要素を含めてください。
              テーマ：{answer}
              含めてほしい要素：{words}
              """

    response = generate_image_api(prompt)
    image_url = response.data[0].url

    return image_url

# 画像を保存する関数
def save_image(image, filename):

    # 画像データを取得
    image_data = requests.get(image).content

    # 画像ファイルとして保存
    with open(filename, "wb") as image_file:
        image_file.write(image_data)

    print(f"画像が '{filename}' として保存されました。")

# ファイル名を決定するための関数
def get_next_filename(directory, base_name, extension):
    i = 1
    while True:
        filename = os.path.join(directory, f"{base_name}{i}.{extension}")
        if not os.path.exists(filename):
            return filename
        i += 1

# データの収納
def create_dataset(answer, image, candidates, features):
    # 新しいデータのセット
    new_data = {
        "answer": answer,
        "image": image,
        "candidates": candidates,
        "features": features
    }
    
    # stockディレクトリのパス
    stock_dir = '../image_stock'
    
    # stockディレクトリが存在しない場合は作成
    if not os.path.exists(stock_dir):
        os.makedirs(stock_dir)
        
    # stockディレクトリ内のstock.jsonファイルのパス
    stock_json_path = os.path.join(stock_dir, 'image_stock.json')
    
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
        
        return print("データが保存されました。")
    else:
        return print("同じanswerを持つデータが既に存在します。追加しませんでした。")

# main文
def main():

    # 画像の生成
    words = generate_words()
    print(words)
    image = generate_image(words)

    # 画像生成と保存の実行
    directory = "../image_stock"
    base_name = "image"
    extension = "png"
    
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # 次のファイル名を取得
    filename = get_next_filename(directory, base_name, extension)

    # 画像を保存
    save_image(image, filename)

    # データを保存
    filename = filename.replace(f"{directory}/", "")
    create_dataset(answer, filename)

# 実行
if __name__ == "__main__":
    main()