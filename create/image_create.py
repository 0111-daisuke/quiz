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
        temperature = 0.5,
        max_tokens = 300
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

# 回答候補生成用の設定
def generate_candidates_api(image):
    return client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text",
         "text": """この画像から考えられることわざを5つ挙げて下さい。
         """},
        {
          "type": "image_url",
          "image_url": {
            "url": image,
          },
        },
      ],
    }
  ],
  max_tokens=300
)

# 画像の特徴生成用の設定
def generate_features_api(image):
    return client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text",
         "text": """
         以下の例を参考にこの画像の特徴を5つ挙げて下さい。
         ---------------
         【例】
         幻想的なデザイン: 巨大な鳥が人をつかんでいるという非現実的なシーンが描かれています。全体的に幻想的で夢のような雰囲気があります。
         詳細なイラスト: 鳥や人物、背景の木々、雲などが非常に細かく描かれており、緻密な線画のスタイルが特徴的です。
         鮮やかな色使い: 鳥の羽や空の色、雲などが鮮やかな色で塗られており、視覚的に強いインパクトがあります。
         シンボリックな要素: 鳥が何かをくわえて飛んでいることや、人物が小島に立っていることなど、シンボリックな要素が含まれており、ストーリー性を感じさせます。
         自然と人間の対比: 巨大な鳥と小さな人間という対比が強調されており、自然と人間の関係性を示唆しているように見えます。背景には海と木々があり、自然環境が大きなテーマとなっています。
         ---------------
         """},
        {
          "type": "image_url",
          "image_url": {
            "url": image,
          },
        },
      ],
    }
  ],
  max_tokens=300
)

# 物語生成
def generate_story():
    
    # 物語を生成するプロンプト
    story_create_messages = [
        {"role": "system",
         "content": f"""
         以下のことわざを基に200字程度の物語を考えてください。
         ことわざ:{answer}
         以下は物語の生成例です。これを参考にして物語を考えてください。
         -------------------------------
         【例】
         ことわざ: 三人寄れば文殊の知恵
         昔々、小さな山里の村が山崩れで外界と隔絶され、食料が底をつきました。村の長老は三人の若者に協力を促し、それぞれが得意分野を活かして問題解決を始めました。一人は裏道を探索し、もう一人は動物の食料を調べ、最後の一人は簡易の橋を作り道を開通。三人の知恵を合わせ、村は食料を確保し、外界とのつながりを取り戻しました。この話は「三人寄れば文殊の知恵」として教訓となりました。
         -------------------------------
         """}
        ]

    response = word_create_api(story_create_messages)
    story = response.choices[0].message.content

    return story

# プロンプト生成
def generate_prompt(story):
    
    # 物語から画像生成のためのプロンプトを生成するプロンプト
    prompt_create_messages = [
        {"role": "system",
         "content": f"""
         あなたは与えられた物語から画像生成のためのプロンプトを考えてください。
         以下はあることわざを基とした物語とプロンプトの生成例です。これを参考にプロンプトを考えてください。
         -------------------------------
         【物語の例】
         ことわざ: 三人寄れば文殊の知恵
         昔々、小さな山里の村が山崩れで外界と隔絶され、食料が底をつきました。村の長老は三人の若者に協力を促し、それぞれが得意分野を活かして問題解決を始めました。一人は裏道を探索し、もう一人は動物の食料を調べ、最後の一人は簡易の橋を作り道を開通。三人の知恵を合わせ、村は食料を確保し、外界とのつながりを取り戻しました。この話は「三人寄れば文殊の知恵」として教訓となりました。
         【プロンプトの生成例】
         "In a mountainous village, three young villagers—one skilled in climbing, one knowledgeable about plants, and another adept at crafting—are working together. They are surrounded by dense forest, rocky paths, and fallen trees. One is scouting a rocky hill, the other is inspecting edible plants, and the third is building a simple wooden bridge. The scene captures their teamwork and determination in a tranquil, natural setting with morning light breaking through the trees. The image reflects a blend of Japanese folklore and rustic, peaceful scenery."
         -------------------------------
         以下の物語のプロンプトを考えてください
         {story}
         """}
        ]

    response = word_create_api(prompt_create_messages)
    prompt = response.choices[0].message.content

    return prompt

# 画像を生成する関数
def generate_image(prompt):

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

# 回答候補の生成
def generate_candidates(image):
    response = generate_candidates_api(image)

    candidates = response.choices[0].message.content
    candidates = ' '.join(candidates)
    candidates = candidates.replace(" ", "")
    candidates = candidates.replace("\n", "")
    candidates = candidates.split("ことわざ")

    return candidates


# 特徴の生成
def generate_features(image):
    response = generate_features_api(image)

    features = response.choices[0].message.content
    features = ' '.join(features)
    features = features.replace(" ", "")
    features = features.replace("\n", "")
    features = features.split("特徴")

    return features

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
    stock_dir = '../stock'
    
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
        
        return print("データが保存されました。")
    else:
        return print("同じanswerを持つデータが既に存在します。追加しませんでした。")

# main文
def main():

    # 画像の生成
    story = generate_story()
    print(story)
    prompt = generate_prompt(story)
    print(prompt)
    image = generate_image(prompt)

    # 画像生成と保存の実行
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

    # 回答候補と特徴の生成
    candidates = generate_candidates(image)
    features = generate_features(image)

    # データをまとめて保存
    filename = filename.replace(f"{directory}/", "")
    create_dataset(answer, filename, candidates, features)


# 実行
if __name__ == "__main__":
    main()