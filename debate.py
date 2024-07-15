from openai import OpenAI
import random

client = OpenAI()

# host
def host_api(messages):
    return client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        temperature=1.0,
        max_tokens=30
        )

# gest
def gest_api(messages):
    return client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        temperature=0.5,
        max_tokens=30
        )

# branch
def branch_api(messages):
    return client.chat.completions.create(
        model = "gpt-4o",
        messages = messages,
        temperature = 1.0,
        max_tokens = 1
        )

def branch(word, talk):

    branch_messages = [
        {"role": "system", "content": f"次の文に{word}が含まれていた場合0を、含まれていない場合1を返してください。"}
        ]
    
    branch_messages.append({"role": "user", "content": talk})
    branch_response = branch_api(branch_messages)
    res = branch_response.choices[0].message.content
    return res

# main文
def main():
    theme = "「地球温暖化」"

    # hostのプロンプト
    host_messages = [
        {"role": "system", "content": "あなたはuserとgestが行っているディベートの司会をしてください。"},
        {"role": "system", "content": f"題目は{theme}についてです。"}
        ]
    
    # gestのプロンプト
    gest_messages = [
        {"role": "system", "content": "あなたはhostを交えてuserとディベートをしてください。"},
        {"role": "system", "content": f"題目は{theme}についてです。"}
        ]
    
    user_input = ""  # user_input変数を初期化

    # 冒頭1会話目
    response1 = host_api(host_messages)
    res1 = response1.choices[0].message.content
    print("host:"+res1)
    
    # 確率
    user_probability = 0.5
    
    talk = ""

    while True:
        word = "天気"
        n = int(branch(word, talk))
        print(type(n))

        if n == 0:
            print("end")
            break

        # exitと打てば終了
        if user_input.lower() == "exit":
            break

        #ランダムにuserかgestが会話
        if random.choices([True, False], weights=[user_probability, 1 - user_probability])[0]:
            # user
            user_input = input("user: ")
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
            
        # 司会AIの受け答え
        response3 = host_api(host_messages)
        res3 = response3.choices[0].message.content
        host_messages.append({"role": "assistant", "content": res3})
        print("host:"+res3)
        
        # 1ループ目の会話を保存
        res1 = res3
        talk = res3

if __name__ == "__main__":
    main()

