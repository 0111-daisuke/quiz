from openai import OpenAI
import random
import json
import os
import re

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
        temperature = 1,
        max_tokens = 100
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
    return data[8]

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

def branch(messages):
        # 次に誰が発話するかの判定
        branch = client.chat.completions.create(
        model = "gpt-4o",
        messages = messages
        )

        branch = branch.choices[0].message.content
        branch = branch.lower()

        # 最初に出現する h, g, u に基づいて変数を設定
        first_char = None
        for char in branch:
            if char in ('h', 'g', 'u'):
                first_char = char
                break

        # 最初に出てくる文字によって次の発話者を決定
        if first_char == 'h':
            variable = "host"
        elif first_char == 'g':
            variable = "guest"
        elif first_char == 'u':
            variable = "user"
        else:
            variable = "unknown"

        return variable

# main文
def main():
    # データの取得
    answer, image, candidates, feature = theme()

    print(image)

    # hostのプロンプト
    host_messages = [
            {
            "role": "system", 
            "content": f"""
                        あなたはUserとGuestが行っている画像を使用したクイズの司会(Host)です。
                        以下の点に気を付けて発言してください。
                        1.正解は当てられるまで言わない
                        2.友達口調で発言する
                        3.ヒントを求められたら画像の特徴を参考にして教える
                        4.会話は100文字以内にまとめる

                        今回の問題を示します。
                        【問題】
                        正解:{answer}
                        画像の特徴:{feature}
                        --------------------------
                        以下は対話履歴です。これらの文章に続くように発言してください。
                        【対話履歴】
                        """
            }
        ]

    # guestのプロンプト
    guest_messages = [
        {
        "role": "system",
        "content": f"""
                    あなたは司会であるHostによって提示された画像を見て元となったことわざを当てるクイズに参加しています。
                    あなたはGuestとして参加しています。もう一人の回答者であるUserを楽しませられるように行動します。
                    以下の点に気を付けて発言してください。
                    1.正解は言わない
                    2.友達口調で発言する
                    3.他の参加者と話をしつつ根拠を交えて回答する
                    4.同じ回答の候補を使わない
                    5.会話は100文字以内にまとめる

                    今回の問題を示します。
                    【問題】
                    正解:{answer}
                    回答候補:{candidates}
                    画像の特徴:{feature}
                    --------------------------
                    以下は対話履歴です。これらの文章に続くように発言してください。
                    【対話履歴】
                    """
        }
    ]

    # 次話者決定
    branch_messages = [
        {"role": "system", 
         "content": f"""
                    これはHostが出題するクイズにUserとGuestが答える文です。
                    あなたはこの対話履歴を見て文脈を考慮したうえで誰が次に喋るか予想して教えてください。
                    また、そう予想した理由を答えてください。

                    以下は対話履歴です。
                    【対話履歴】
                    """}
        ]

    # プロンプトに文章を追加する関数
    def append_message(user1, user2, res):
        host_messages.append({"role": user1, "content": res})
        guest_messages.append({"role": user2, "content": res})
        branch_messages.append({"role": "user", "content": res})

    # 最初にuserが会話する確率
    user_probability = 0.7

    # 変数の初期化
    user_input = ""
    n = 0

    # 初期情報の保存
    log = "off_example_quiz.py\n"
    log += f'img:{image}, user_probability:{user_probability}\n'

    # 1文目
    res = "Host:では問題です、この画像は何ということわざをテーマに生成されたでしょう"
    # プロンプトに文章を追加
    append_message("assistant", "user", res)
    # 保存
    log += res
    # 表示
    res = re.sub(r'^(Host:)+', '', res)
    print(green + "Host:" + color_end + res)

    # ランダムにUserかGuestが会話
    if random.choices([True, False], weights = [user_probability, 1 - user_probability])[0]:
        # User
        user_input = input("User: ")
        # プロンプトに文章を追加
        res = "User:" + user_input
        append_message("user", "user", res)
        # 保存
        log += "\n" + res

    else:
        # Guest
        response = guest_api(guest_messages)
        res = response.choices[0].message.content
        # 表示
        res = re.sub(r'^(Guest:)+', '', res)
        print(blue + "Guest:" + color_end + res)
        # プロンプトに文章を追加
        res = "Guest:" + res
        append_message("user", "assistant", res)
        # 保存
        log += "\n" + res

    # ループ
    while True:

        next_talk = branch(branch_messages)

        # 3回unkownになったらerror
        if next_talk == "unknown":
            n += 1
            if n == 3:
                print("branch error")
                break

        elif  next_talk == "host":
            # Host
            response = host_api(host_messages)
            res = response.choices[0].message.content
            # 表示
            res = re.sub(r'^(Host:)+', '', res)
            print(green + "Host:" + color_end + res)
            # プロンプトに文章を追加
            res = "Host:" + res
            append_message("assistant", "user", res)
            # 保存
            log += "\n" + res
            # Userが正解したらHostの返答後終了
            if answer in user_input:
                save_to_log(log)
                break

        elif next_talk == "guest":
            # Guest
            response = guest_api(guest_messages)
            res = response.choices[0].message.content
            # 表示
            res = re.sub(r'^(Guest:)+', '', res)
            print(blue + "Guest:" + color_end + res)
            # プロンプトに文章を追加
            res = "Guest:" + res
            append_message("user", "assistant", res)
            # 保存
            log += "\n" + res

        elif next_talk == "user":
            # User
            user_input = input("User:")
            # プロンプトに文章を追加
            res = "User:" + user_input
            append_message("user", "user", res)
            # 保存
            log += "\n" + res

# 実行
if __name__ == "__main__":
    main()