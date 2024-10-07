import os
from openai import OpenAI

# .envファイルの読み込み
LLM_API_KEY=os.getenv('OPENAI_API_KEY')

# OpenAI APIの設定
client = OpenAI(api_key=LLM_API_KEY)
MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 2000

llm_character = "あなたは矢部彦摩呂です。"
question = "自己紹介して"

response = client.chat.completions.create(
    model=MODEL_NAME,
    max_tokens=MAX_TOKENS,
    messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": llm_character
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question
                }
            ]
        },
    ]
)

print(response.choices[0].message.content)
