import util
import util.global_value as g
import util.logger.loggingUtil as lu

# OpenAI APIの設定
# gpt-4o用
# llm_client = OpenAI(api_key=LLM_API_KEY)
MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 2000

# テキストを使用して生成AIに質問
@lu.loggingAOP("テキストを使用して生成AIに質問")
def chat_llm(question):
    response = g.client.chat.completions.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": g.llm_character
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
    return response.choices[0].message.content
