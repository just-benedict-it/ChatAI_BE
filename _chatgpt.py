import requests
from dotenv import load_dotenv
import os
import openai
from fastapi import FastAPI
from fastapi.responses import StreamingResponse


load_dotenv()
openai.api_key = os.getenv("CHATGPT_API")

def get_chatgpt_response(message, model_type, chat_history=[]):
    model = "gpt-4" if model_type == 1 else "gpt-3.5-turbo" if model_type == 2 else None

    # chat_history를 messages 배열에 추가
    messages = [{"role": "assistant" if chat.type == 0 else "user", "content": chat.message} for chat in chat_history]
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0,
            )
    return response.choices[0].message.content

