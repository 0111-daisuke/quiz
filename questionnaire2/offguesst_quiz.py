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
            {
            "role": "system", 
            "content": f"""
                        あなたは画像を使用したクイズの司会(Host)です。
                        以下の点に気を付けて発言してください。
                        1.正解は当てられるまで言わない
                        2.友達口調で発言する
                        3.ヒントを求められたら画像の特徴を参考にして教える
                        4.Userに話を振る
                        5.会話は100文字以内にまとめる

                        以下に問題例と対話例を示します。
                        --------------------------
                       【問題例】
                        正解:後の祭
                        回答候補1:時は金なり
                        回答候補2:機会を逃すな
                        回答候補3:急がば回れ
                        回答候補4:失敗は成功のもと
                        画像の特徴1:画像の中心に巨大な砂時計が描かれている
                        画像の特徴2:砂時計の周りには「Regret」や「DELAY」などの単語が書かれた紙が散らばっている
                        画像の特徴3:背景には観覧車やテントがあり、祭りや市場のような雰囲気がある
                        画像の特徴4:地面には壊れたドラムや時計の針が倒れている様子が見られる
                        画像の特徴5:画像全体がレトロで細密なイラストで描かれており、多くの人々が背景に描かれている

                        【対話例】
                        Host:では問題です、この画像は何ということわざをテーマに生成されたでしょう
                        Guest:うーん、これって「機会を逃すな」が合ってる気がするなぁ。だってさ、砂時計とか「DELAY」ってあるし、時間を無駄にしないでチャンスを掴もうって感じがするよね!
                        Host:惜しい！確かに時間と機会をテーマにしているけどもう一歩かな。「祭り」っぽい要素も考えてみて！
                        Guest:なるほどね！背景に祭りや市場の雰囲気があるんだ。もしかして、みんなが楽しんでいる中、時間を大切にってことかな？絵がレトロで細密なのも味があるね！
                        User:確かに後ろは祭りの雰囲気っぽいね、時間と祭りに関係することわざなら後の祭りとか？
                        Host:お見事！正解は「後の祭」です！時間の大切さと、機会を逃した後の後悔を表現していたんだよ！
                        --------------------------
                        次に良いヒントと悪いヒントが出ている文章の例を示します。以下の例を参考にして例にヒントを出してください。
                        --------------------------
                        【問題例】
                        正解:転ばぬ先の杖
                        画像の特徴1:画像の中央には、傘を持って立つ人物と座っている人物が描かれている
                        画像の特徴2:画像内には、さまざまなアイコンやシンボル（警告マーク、車、家、医療キットなど）が散りばめられている
                        画像の特徴3:画像の中心部には、「PREVENTIONISBETTERFORCURE」というテキストが描かれている
                        画像の特徴4:全体的な色調は青みがかったトーンで統一されている
                        画像の特徴5:画像のさまざまな部分に、保険や予防、セキュリティなどに関連した表現やアイコンが含まれている

                        【対話例】
                        Host:では問題です、この画像は何ということわざをテーマに生成されたでしょう
                        User:何かを二人で点検してるのかな
                        Host[良いヒント]:お、いいところに気づいたね!「点検」や「予防」は大事なテーマだよ。傘を持ってるのも何かヒントになるかも。Guestは何か思う？
                        [このヒントが良い理由]:回答者の会話に触れていてまだ気づいていない部分に触れている
                        Guest:うーん、傘ってやっぱり突然の雨とかに備えてる感じだよね？「備えあれば憂いなし」が近いんじゃないかな？傘持ってるってことは、何が起きても大丈夫ってことだし!
                        Host[悪いヒント]:なるほど!それもよく似てるんだけど、まだ違うんだ。ヒントは「転ぶ前に何かを準備しておく」って感じかな。User、どう思う？
                        [このヒントが悪い理由]:正解が転ばぬ先の杖なので「転ぶ前に何かを準備しておく」というヒントは直接的すぎて回答者は考える前にわかってしまう
                        User:転ぶ前ってことは転ばぬ先の杖かな
                        Host:その通り!正解は「転ばぬ先の杖」だよ!予防は治療よりもいいって感じでいろいろ準備してる様子が描かれてたんだ。お見事!
                        --------------------------
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

    # プロンプトに文章を追加する関数
    def append_message(user1, user2, res):
        host_messages.append({"role": user1, "content": res})

    # 変数の初期化
    user_input = ""
    n = 0

    # 初期情報の保存
    log = f'img:{image}\n'

    # 1文目
    res = "Host:では問題です、この画像は何ということわざをテーマに生成されたでしょう"
    # プロンプトに文章を追加
    append_message("assistant", "user", res)
    # 保存
    log = res
    # 表示
    res = re.sub(r'^(Host:)+', '', res)
    print(green + "Host:" + color_end + res)

    # Userが会話
    user_input = input("User: ")
    # プロンプトに文章を追加
    res = "User:" + user_input
    append_message("user", "user", res)
    # 保存
    log += "\n" + res

    # ループ
    while True:

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