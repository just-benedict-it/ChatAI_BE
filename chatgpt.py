import requests
from dotenv import load_dotenv
import os
import openai
from itertools import cycle
import time

load_dotenv()
api_keys = [
    os.getenv("CHATGPT_API_1"),
    os.getenv("CHATGPT_API_2"),
    os.getenv("CHATGPT_API_3"),
    # 필요한 만큼 더 추가할 수 있습니다.
]

# API 키들을 순환할 수 있는 이터레이터를 생성합니다.
api_key_cycle = cycle(api_keys)

def get_next_api_key():
    """
    API 키 리스트에서 다음 API 키를 가져옵니다.
    """
    global api_key_cycle
    return next(api_key_cycle)

async def get_chatgpt_response(message, model_type, chat_history=[]):
    # 다음 API 키를 가져옵니다.
    api_key = get_next_api_key()

    # openai 라이브러리에 API 키 설정
    openai.api_key = api_key

    if model_type == 1:
        model = "gpt-4-1106-preview"
        request_timeout = 25  # GPT-4 모델에 대한 타임아웃
    elif model_type == 2:
        model = "gpt-3.5-turbo-1106"
        request_timeout = 15  # GPT-3.5 모델에 대한 타임아웃
    else:
        model = None
        request_timeout = None
        
    # chat_history를 messages 배열에 추가
    messages = [{"role": "assistant" if chat.type == 0 else "user", "content": chat.message} for chat in chat_history]
    messages.append({"role": "user", "content": message})


    response = None
    retries = 3    
    while retries > 0: 
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0,
                request_timeout=request_timeout,
                max_tokens = 1024
            )
            break  # 성공적으로 응답을 받았으므로 반복문 탈출
        except Exception as e:    
            print(e)   
            print('Timeout error, retrying...')    
            retries -= 1    
            time.sleep(2)    

    if response:
        return response.choices[0].message.content
    else: 
        return "Please try later"
