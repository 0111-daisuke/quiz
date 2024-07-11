from openai import OpenAI

client = OpenAI()

def branch_api(messages):
    return client.chat.completions.create(
        model = "gpt-4o",
        messages = messages,
        temperature = 1,
        max_tokens = 5
        )

def branch(word):

    branch_messages = [
        {"role": "system", "content": f"次の文に{word}が含まれていた場合0を、含まれていない場合1を返してください。"}
        ]
    
    user_input = input("user: ")
    branch_messages.append({"role": "user", "content": user_input})
    branch_response = branch_api(branch_messages)
    res = branch_response.choices[0].message.content

    print(res)

def main():
    word = "ことわざ"
    branch(word)

# 実行
if __name__ == "__main__":
    main()
    

