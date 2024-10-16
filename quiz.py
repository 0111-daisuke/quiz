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
        model = "gpt-4o",
        messages = messages,
        temperature = 1,
        max_tokens = 100
        )

# guestのAPI
def guest_api(messages):
    return client.chat.completions.create(
        model = "gpt-4o",
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
def branch(host_words, talk):

    branch_messages = [
        {"role": "system", 
         "content": f"次の文に{host_words}が含まれていた場合0を、含まれていない場合1を返してください。"}
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
            {"role": "system", 
              "content": "あなたはhostとしてuserとguestが行っている画像を使用したクイズの司会をしてください。"
                         f"このクイズの正解は{answer}です。友達口調でuserの文章に反応するようにしてください。"
                         "クイズの正解はuserが当てるまで直接喋らないでください。"
                         f"画像の特徴は以下のようになっています。{feature}これらを参考にヒントを出しつつ進行してください。"
                         "画像を直接見れないことに触れないでください。"
                         "会話は100文字以内にまとめてください。"
            }
        ]

    # guestのプロンプト
    guest_messages = [
        {"role": "system",
         "content": f"あなたはguestとしてこの特徴{feature}からどのことわざが適切か答えるクイズに答えてください。"
                    "友達口調で文章に反応するようにしてください。"
                    f"回答の候補は以下に記します。{candidates}"
                    "他の参加者と話をしつつ回答の候補から根拠を交えてランダムに答えて下さい。"
                    "同じ回答の候補を使わないでください。"
                    "会話は100文字以内にまとめてください。"
        }
    ]

    # guestがhostと対話する時のプロンプト
    guest_reply = [
        {"role": "system",
         "content": "あなたはguestとして最後の文章に続くように文章を返してください。"
                    "友達口調で文章に応答するようにしてください。"
                    "**文章にはことわざを使用しないでください。**"
                    "会話は100文字以内にまとめてください。"
        }
    ]

    # userが会話する確率
    user_probability = 0.7

    # 変数の初期化
    user_input = ""

    # hostを呼び出すためのワード
    host_words = [
        "ことわざ",
        "四字熟語",
        "ヒントを求める文章",
        "hostという言葉が含まれている文章"
        ]

    # guestを呼び出すためのワード
    guest_words = [
        "guestという言葉が含まれている文章"
        ]

    log = f'img:{image}, user_probability:{user_probability}\n'

    res1 = "では問題です、この画像は何ということわざをテーマに生成されたでしょう"
    print(green + "host:" + color_end + res1)
    log += 'host:' + res1

    # プロンプトに文章を追加
    host_messages.append({"role": "assistant", "content": res1})
    guest_messages.append({"role": "user", "content": res1})
    guest_reply.append({"role": "user", "content": res1})

    # ランダムにuserかguestが会話
    if random.choices([True, False], weights = [user_probability, 1 - user_probability])[0]:
        # user
        user_input = input("user: ")
        log += '\nuser:' + user_input
        put = user_input
        # プロンプトに文章を追加
        host_messages.append({"role": "user", "content": put})
        guest_messages.append({"role": "user", "content": put})
        guest_reply.append({"role": "user", "content": put})

    else:
        # guest
        response2 = guest_api(guest_messages)
        res2 = response2.choices[0].message.content
        print(blue + "guest:" + color_end + res2)
        log += "\nguest:" + res2
        put = res2
        # プロンプトに文章を追加
        host_messages.append({"role": "user", "content": put})
        guest_messages.append({"role": "assistant", "content": put})
        guest_reply.append({"role": "assistant", "content": put})

    # hostが発話するかの判定
    n = branch(host_words, put)

    # ループ
    while True:

        # 会話にhost_wordsに関する文章が含まれていたらhostが判定
        if  n == 0:
            # host
            response3 = host_api(host_messages)
            res3 = response3.choices[0].message.content
            print(green + "host:" + color_end + res3)
            log += "\nhost:" + res3
            n = 1
            # 会話を保存
            res1 = res3
            # プロンプトに文章を追加
            host_messages.append({"role": "assistant", "content": res1})
            guest_messages.append({"role": "user", "content": res1})
            guest_reply.append({"role": "user", "content": res1})

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
                log += '\nuser:' + user_input
                put = user_input
                # プロンプトに文章を追加
                host_messages.append({"role": "user", "content": put})
                guest_messages.append({"role": "user", "content": put})
                guest_reply.append({"role": "user", "content": put})

            elif put == res2:
                # guest
                response2 = guest_api(guest_reply)
                res2 = response2.choices[0].message.content
                print(blue + "guest:" + color_end + res2)
                log += "\nguest:" + res2
                put = res2
                # プロンプトに文章を追加
                host_messages.append({"role": "user", "content": put})
                guest_messages.append({"role": "assistant", "content": put})
                guest_reply.append({"role": "assistant", "content": put})

        elif n == 1:
            # 前の会話がuserだったらguestが発話
            if put == user_input:
                # guest
                response2 = guest_api(guest_messages)
                res2 = response2.choices[0].message.content
                print(blue + "guest:" + color_end + res2)
                log += "\nguest:" + res2
                put = res2
                # プロンプトに文章を追加
                host_messages.append({"role": "user", "content": put})
                guest_messages.append({"role": "assistant", "content": put})
                guest_reply.append({"role": "assistant", "content": put})

            # 前の発話がguestだったらuserが発話
            elif put == res2:
                # user
                user_input = input("user: ")
                # exitと打って終了
                if user_input.lower() == "exit":
                    break
                log += '\nuser:' + user_input
                put = user_input
                # プロンプトに文章を追加
                host_messages.append({"role": "user", "content": put})
                guest_messages.append({"role": "user", "content": put})
                guest_reply.append({"role": "user", "content": put})

            # hostが発話するかの判定
            n = branch(host_words, put)

# 実行
if __name__ == "__main__":
    main()