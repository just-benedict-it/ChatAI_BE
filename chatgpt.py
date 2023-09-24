import requests
from dotenv import load_dotenv
import os
import openai


load_dotenv()
openai.api_key = os.getenv("CHATGPT_API")

def get_chatgpt_response(message, chat_history=[]):
    # chat_history를 messages 배열에 추가
    messages = [{"role": "assistant" if chat.type == 0 else "user", "content": chat.message} for chat in chat_history]
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0,
            )
    return response.choices[0].message.content
