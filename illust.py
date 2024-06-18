import openai
import requests
import os

import base64

# OpenAI APIキーを環境変数から取得
openai.api_key = os.getenv("OPENAI_API_KEY")

# 画像を生成して保存する関数
def generate_and_save_image(prompt, filename):
    client = openai.OpenAI()

    # 画像生成のリクエスト
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # 生成された画像のURLを取得
    image_url = response.data[0].url

    # 画像データを取得
    image_data = requests.get(image_url).content

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

# 画像生成と保存の実行例
prompt = "ことわざ「蛙の子は蛙」"
directory = "stock"
base_name = "image"
extension = "png"

# ディレクトリが存在しない場合は作成
if not os.path.exists(directory):
    os.makedirs(directory)

# 次のファイル名を取得
filename = get_next_filename(directory, base_name, extension)

# 画像を生成して保存
generate_and_save_image(prompt, filename)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')