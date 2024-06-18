import openai
import os
import random

# OpenAIのAPIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response_from_gpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # モデル名は適宜調整
        messages=messages,
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()

def game_conversation(host_prompt, participant_prompt, user_turns=5, user_probability=0.6):
    messages = [
        {"role": "system", "content": "あなたはゲームの司会者です。"},
        {"role": "user", "content": host_prompt},
        {"role": "assistant", "content": participant_prompt}
    ]

    for i in range(user_turns):
        # ゲームの司会の応答
        messages.append({"role": "user", "content": "ゲームの司会:"})
        host_response = get_response_from_gpt(messages)
        print(f"ゲームの司会: {host_response}")
        messages.append({"role": "assistant", "content": host_response})

        # 参加者とユーザーのどちらが応答するかを確率で選択
        if random.choices([True, False], weights=[user_probability, 1 - user_probability])[0]:
            # ユーザーの入力
            user_input = input("あなた: ")
            messages.append({"role": "user", "content": f"ユーザー: {user_input}"})
        else:
            # 参加者の応答
            messages.append({"role": "user", "content": "ゲームの参加者:"})
            participant_response = get_response_from_gpt(messages)
            print(f"ゲームの参加者: {participant_response}")
            messages.append({"role": "assistant", "content": participant_response})

if __name__ == "__main__":
    # 初期プロンプトを設定
    host_initial_prompt = "こんにちは、私はゲームの司会者です。今日は楽しいゲームを進行します。準備はいいですか？"
    participant_initial_prompt = "こんにちは、ゲームの参加者です。よろしくお願いします。"

    # ゲームの会話を開始 (ユーザーが60%の確率で応答)
    game_conversation(host_initial_prompt, participant_initial_prompt, user_turns=5, user_probability=0.6)
