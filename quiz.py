from openai import OpenAI
import random
import json
import os

client = OpenAI()
file_path = "stock/stock.json"
green = "\033[32m"
blue = "\033[34m"
color_end = "\033[0m"

# hostのAPI
def host_api(messages):
    return client.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages = messages,
        temperature = 1,
        max_tokens = 100
        )

# guestのAPI
def guest_api(messages):
    return client.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages = messages,
        temperature = 0.3,
        max_tokens = 100
        )

# 分岐システムのAPI
def branch_api(messages):
    return client.chat.completions.create(
        model = "gpt-4o",
        messages = messages,
        temperature = 1,
        max_tokens = 1
        )

# 分岐システム
def branch(words, talk):

    branch_messages = [
        {"role": "system", "content": f"次の文に{words}が含まれていた場合0を、含まれていない場合1を返してください。"}
        ]
    
    branch_messages.append({"role": "user", "content": talk})
    branch_response = branch_api(branch_messages)
    res = branch_response.choices[0].message.content
    return int(res)

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

# logディレクトリにファイルを作成
def make_log_file():
    i = 1
    while True:
        filename = f"quizlog{i}.txt"
        filepath = os.path.join('log', filename)
        if not os.path.exists(filepath):
            return filepath
        i += 1

# logディレクトリに作成したファイルに保存
def save_to_log(log):
    # ファイル作成
    next_filename = make_log_file()

    # txt形式にするために文章を''で囲む
    log = ' '.join(log)
    log = log.replace(" ", "")

    # ファイルにテキストを書き込む
    with open(next_filename, 'w', encoding='utf-8') as file:
        file.write(log)

    # 完了メッセージ
    print(f"テキストは {next_filename} に保存されました。")

# main文
def main():
    # データの取得
    answer, image, candidates, feature = theme()

    print(image)

    # hostのプロンプト
    host_messages = [
        {"role": "system", "content": "あなたはhostとしてuserとguestが行っている画像を使用したクイズの司会をしてください。"},
        {"role": "system", "content": f"このクイズの正解は{answer}にです。"},
        {"role": "system", "content": "友達口調でuserの文章に反応するようにしてください"},
        {"role": "system", "content": "クイズの正解はuserが当てるまで直接喋らないでください。"},
        {"role": "system", "content": "画像の特徴は以下のようになっています。これらを参考にヒントを出しつつ進行してください。"},
        {"role": "system", "content": feature},
        {"role": "system", "content": "画像を直接見れないことに触れないでください。"},
        {"role": "system", "content": "会話は100文字以内にまとめてください。"}
        ]
    
    # guestのプロンプト
    guest_messages = [
        {"role": "system", "content": "あなたはguestとして画像を見て答えるクイズに答えてください。"},
        {"role": "system", "content": "友達口調でuserの文章に反応するようにしてください"},
        {"role": "system", "content": "回答の候補は以下に記します。他の参加者と話をしつつこれらの回答から根拠を交えてランダムに答えて下さい。"},
        {"role": "system", "content": candidates},
        {"role": "system", "content": "同じ回答の候補を使わないでください。"},
        {"role": "system", "content": "画像の特徴は以下のようになっています。これらを根拠として活用してください。"},
        {"role": "system", "content": feature},
        {"role": "system", "content": "画像を直接見れないことに触れないでください。"},
        {"role": "system", "content": "会話は100文字以内にまとめてください。"}
        ]
    
    guest_reply = [
        {"role": "system", "content": "あなたはguestとして画像を見て答えるクイズに答えてください。"},
        {"role": "system", "content": "友達口調でuserの文章に反応するようにしてください"},
        {"role": "system", "content": "画像の特徴は以下のようになっています。これらを根拠として活用してください。"},
        {"role": "system", "content": feature},
        {"role": "system", "content": "画像を直接見れないことに触れないでください。"},
        {"role": "system", "content": "会話は100文字以内にまとめてください。"}
        ]
    
    # userが会話する確率
    user_probability = 0.7
    
    # 変数の初期化
    user_input = ""
    words = [
        "ことわざ",
        "ヒントを求める文章",
        "hostという言葉が含まれている文章"
        ]
    
    log = f'img:{image}, user_probability:{user_probability}\n'

    res1 = "では問題です、この画像は何ということわざをテーマに生成されたでしょうか"
    print(green + "host:" + color_end + res1)
    log += 'host:' + res1

    # ランダムにuserかguestが会話
    if random.choices([True, False], weights = [user_probability, 1 - user_probability])[0]:
        # user
        user_input = input("user: ")
        log += '\nuser:' + user_input
        put = user_input

    else:
        # guest
        guest_messages.append({"role": "assistant", "content": res1})
        response2 = guest_api(guest_messages)
        res2 = response2.choices[0].message.content
        print(blue + "guest:" + color_end + res2)
        log += "\nguest:" + res2
        put = res2

    # ループ
    while True:
        # ことわざの有無を判定
        n = branch(words, put)
    
        # 会話にことわざが含まれていたらhostが判定
        if  n == 0:
            # hostの返答
            host_messages.append({"role": "user", "content": put})
            response3 = host_api(host_messages)
            res3 = response3.choices[0].message.content
            host_messages.append({"role": "user", "content": res3})
            print(green + "host:" + color_end + res3)
            log += "\nhost:" + res3
            n = 1
            # 会話を保存
            res1 = res3
            # 正解したらhostの返答後終了
            if answer in user_input:
                save_to_log(log)
                break

            if put == user_input:
                # user
                user_input = input("user: ")
                # exitと打って終了
                if user_input.lower() == "exit":
                    break
                guest_messages.append({"role": "user", "content": user_input})
                log += '\nuser:' + user_input
                put = user_input

            elif put == res2:
                # guest
                guest_reply.append({"role": "assistant", "content": res1})
                response2 = guest_api(guest_reply)
                res2 = response2.choices[0].message.content
                print(blue + "guest:" + color_end + res2)
                log += "\nguest:" + res2
                put = res2

        elif n == 1:
            # 前の会話がuserだったらguestが発話
            if put == user_input:
                # guest
                guest_messages.append({"role": "assistant", "content": res1})
                response2 = guest_api(guest_messages)
                res2 = response2.choices[0].message.content
                print(blue + "guest:" + color_end + res2)
                log += "\nguest:" + res2
                put = res2
                
            # 前の発話がguestだったらuserが発話
            elif put == res2:
                # user
                user_input = input("user: ")
                # exitと打って終了
                if user_input.lower() == "exit":
                    break
                guest_messages.append({"role": "user", "content": user_input})
                log += '\nuser:' + user_input
                put = user_input

# 実行
if __name__ == "__main__":
    main()