import openai
import os
import random

# OpenAIのAPIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response_from_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # モデル名は適宜調整
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def game_conversation(host_prompt, participant_prompt, user_turns=5):
    host_message = host_prompt
    participant_message = participant_prompt

    for i in range(user_turns):
        # ゲームの司会の応答
        host_response = get_response_from_gpt(
            f"ゲームの司会: {host_message}\nゲームの参加者: {participant_message}\nゲームの司会: 次の質問に答えてください。『好きな色は何ですか？』"
        )
        print(f"ゲームの司会: {host_response}")
        host_message = host_response

        # 参加者とユーザーのどちらが応答するかをランダムに選択
        if random.choice([True, False]):
            # 参加者の応答
            participant_response = get_response_from_gpt(
                f"ゲームの司会: {host_message}\nゲームの参加者: {participant_message}\nゲームの参加者: その質問は面白いですね！私の答えは『青』です。"
            )
            print(f"ゲームの参加者: {participant_response}")
            participant_message = participant_response
        else:
            # ユーザーの入力
            user_input = input("あなた: ")
            participant_message = f"ユーザー: {user_input}"

if __name__ == "__main__":
    # 初期プロンプトを設定
    host_initial_prompt = "こんにちは、私はゲームの司会者です。今日は楽しいゲームを進行します。準備はいいですか？"
    participant_initial_prompt = "こんにちは、ゲームの参加者です。よろしくお願いします。"

    # ゲームの会話を開始
    game_conversation(host_initial_prompt, participant_initial_prompt)
