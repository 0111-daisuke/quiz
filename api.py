import os
import openai
import json
openai.api_key = "YOUR_OPENAI_API_KEY"

#api一号機
def chatGPT_api_1(messages):
  return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1
    )

#api二号機
def chatGPT_api_2(messages):
  return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5
    )


#api一号機に役割をセット(ポシティブ)
messages_1 = [{"role": "system", "content": "あなたはプロの投資家です。不動産クラウドファンディングににネガティブなことを言われたら30文字以内で反論してください。"}]
response1 = chatGPT_api_1(messages_1)
res1 = response1["choices"][0]["message"]["content"]
print("chatGPT_api_1:"+res1)

#api二号機に役割をセット(ネガティブ)
messages_2 = [{"role": "system", "content": "あなたはプロの投資家です。不動産クラウドファンディングににポシティブなことを言われたら30文字以内で反論してください。"}]
#chatGPT_api_1をuserと見立てて、内容をセット
messages_2.append({"role": "user", "content": response1["choices"][0]["message"]["content"]})
response2 = chatGPT_api_2(messages_2)
res2 = response2["choices"][0]["message"]["content"]
messages_2.append({"role": "assistant", "content": res2})
print("chatGPT_api_2:"+res2)

#今回は２ラウンド議論(自由に決めてください。)
for num in range(2):

  #chatGPT_api_2の回答をセット
  messages_1.append({"role": "user", "content": res2})
  response3 = chatGPT_api_1(messages_1)
  res3 = response3["choices"][0]["message"]["content"]
  #chatGPT_api_1自身の回答も記憶しておく
  messages_1.append({"role": "assistant", "content": response3["choices"][0]["message"]["content"]})
  print("chatGPT_api_1:"+res3)

  #chatGPT_api_1の回答をセット
  messages_2.append({"role": "user", "content": res3})
  response4 = chatGPT_api_2(messages_2)
  #chatGPT_api_2自身自身の回答も記憶しておく
  messages_2.append({"role": "assistant", "content": response4["choices"][0]["message"]["content"]})
  res4 = response4["choices"][0]["message"]["content"]
  print("chatGPT_api_2:"+res4)

  #以後繰り返し
  res2 = res4