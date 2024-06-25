from openai import OpenAI
import requests
import os

client = OpenAI()

candidated = "弘法も筆の誤り"

# 単語生成用API
def word_create_api(messages):
    return client.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages = messages,
        temperature = 0.5,
        max_tokens = 100
        )

# 単語生成
def generate_words(n):
    
    # hostのプロンプト
    words_create_messages = [
        {"role": "system", "content": f"ことわざ{candidated}から連想される単語のみを{n}個出してください"},
        {"role": "system", "content": "出力する際はリンゴ、パイナップルのように並べて出力してください"}
        ]
    
    response = word_create_api(words_create_messages)
    words_list = response.choices[0].message.content

    words_combined = ' '.join(words_list)

    return words_combined

def generate_image_api(prompt):
    return client.images.generate(
        model="dall-e-3",
        prompt=prompt + " without any text or letters.",
        size="1024x1024",
        quality="standard",
        n=1,
        )

# 画像を生成する関数
def generate_image(words):
    prompt = f"ことわざ{candidated}をテーマにした画像を{words}の要素を含めて生成してください。"

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

def main():

    # 画像の生成
    words = generate_words(10)
    print(words)
    image = generate_image(words)

    # 画像生成と保存の実行例
    directory = "../stock"
    base_name = "image"
    extension = "png"
    
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # 次のファイル名を取得
    filename = get_next_filename(directory, base_name, extension)

    # 画像を保存
    save_image(image, filename)

if __name__ == "__main__":
    main()