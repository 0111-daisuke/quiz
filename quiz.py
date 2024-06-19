from openai import OpenAI
import random
import json

client = OpenAI()
file_path = "stock/stock.json"

# 司会側の条件
def host_api(messages):
    return client.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages = messages,
        temperature = 1,
        max_tokens = 300
        )

# 疑似パネリスト側の条件
def gest_api(messages):
    return client.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages = messages,
        temperature = 0.5,
        max_tokens = 300
        )

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

# テーマの取得
def theme():
    random_data = get_random_data()
    
    # 各ステータスを変数に格納
    answer = random_data["answer"]
    image = random_data["image"]
    candidates = random_data["candidates"]
    feature = random_data["features"]

    # messagesに合わせた形式の変換
    candidates = json.dumps(candidates)
    feature = json.dumps(feature)

    return answer, image, candidates, feature

def main():
    # データの取得
    answer, image, candidates, feature = theme()

    # hostのプロンプト
    host_messages = [
        {"role": "system", "content": "あなたはhostとしてuserとgestが行っている画像を使用したクイズの司会をしてください。"},
        {"role": "system", "content": f"このクイズの正解は{answer}にです。"},
        {"role": "system", "content": "クイズの正解はuserが当てるまで直接喋らないでください。"},
        {"role": "system", "content": "画像の特徴は以下のようになっています。これらを参考にヒントを出しつつ進行してください。"},
        {"role": "system", "content": feature},
        {"role": "system", "content": "会話はmax_tokensの文字数以内にまとめてください。"}
        ]
    
    # gestのプロンプト
    gest_messages = [
        {"role": "system", "content": "あなたはgestとして画像を見て答えるクイズに答えてください。"},
        {"role": "system", "content": "回答の候補は以下に記します。これらの回答から根拠を交えてランダムに答えて下さい。"},
        {"role": "system", "content": candidates},
        {"role": "system", "content": "画像の特徴は以下のようになっています。これらを根拠として進行してください。"},
        {"role": "system", "content": feature},
        {"role": "system", "content": "同じ回答の候補を使わないでください。"},
        {"role": "system", "content": "会話はmax_tokensの文字数以内にまとめてください。"}
        ]
    
    # user_input 変数を初期化
    user_input = ""

    # 1会話目
    response1 = host_api(host_messages)
    res1 = response1.choices[0].message.content
    print("host:"+res1)
    
    # userが会話する確率
    user_probability = 0.7

    # ここからループ
    while True:

        # ランダムにuserかgestが会話
        if random.choices([True, False], weights = [user_probability, 1 - user_probability])[0]:
            # user
            user_input = input("user: ")
            # exitと打って終了
            if user_input.lower() == "exit":
                break
            host_messages.append({"role": "user", "content": user_input})
            
        else:
            # gest
            gest_messages.append({"role": "assistant", "content": res1})
            response2 = gest_api(gest_messages)
            res2 = response2.choices[0].message.content
            host_messages.append({"role": "user", "content": res2})
            print("gest:"+res2)
            
        # hostの返答
        response3 = host_api(host_messages)
        res3 = response3.choices[0].message.content
        host_messages.append({"role": "user", "content": res3})
        print("host:"+res3)

        # 正解したらhostの返答後終了
        if answer in user_input:
            break
        
        # 会話を保存
        res1 = res3

if __name__ == "__main__":
    main()