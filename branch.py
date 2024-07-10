from openai import OpenAI
import os

client = OpenAI()

def branch_api(messages):
    return client.chat.completions.create(
        model = "gpt-4-1106-preview",
        messages = messages,
        temperature = 1,
        max_tokens = 5
        )

def main():

    branch_messages = [
        {"role": "system", "content": "次の文にことわざが含まれていた場合0を、含まれていない場合1を返してください。"}
        ]
    
    user_input = input("user: ")
    branch_messages.append({"role": "user", "content": user_input})
    branch_response = branch_api(branch_messages)
    res1 = branch_response.choices[0].message.content

    print(res1)

# 実行
if __name__ == "__main__":
    main()
    

