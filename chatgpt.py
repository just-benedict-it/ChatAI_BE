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

    # model = "gpt-4" if model_type == 1 else "gpt-3.5-turbo" if model_type == 2 else None
    model = "gpt-4-1106-preview" if model_type == 1 else "gpt-3.5-turbo-1106" if model_type == 2 else None

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
                request_timeout=15,
                max_tokens = 256
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

   # except openai.APIError as e:
    #     #Handle API error here, e.g. retry or log
    #     print(f"OpenAI API returned an API Error: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.APIConnectionError as e:
    #     #Handle connection error here
    #     print(f"Failed to connect to OpenAI API: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.RateLimitError as e:
    #     #Handle rate limit error (we recommend using exponential backoff)
    #     print(f"OpenAI API request exceeded rate limit: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.error.Timeout as e:
    #     # Handle timeout error, e.g. retry or log
    #     print(f"OpenAI API request timed out: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.error.APIError as e:
    #     # Handle API error, e.g. retry or log
    #     print(f"OpenAI API returned an API Error: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.error.APIConnectionError as e:
    #     # Handle connection error, e.g. check network or log
    #     print(f"OpenAI API request failed to connect: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.error.APITimeoutError as e:
    #     # Handle connection error, e.g. check network or log
    #     print(f"OpenAI API request failed to connect: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.error.InvalidRequestError as e:
    #     # Handle invalid request error, e.g. validate parameters or log
    #     print(f"OpenAI API request was invalid: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.error.AuthenticationError as e:
    #     # Handle authentication error, e.g. check credentials or log
    #     print(f"OpenAI API request was not authorized: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.error.PermissionError as e:
    #     # Handle permission error, e.g. check scope or log
    #     print(f"OpenAI API request was not permitted: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    # except openai.error.RateLimitError as e:
    #     # Handle rate limit error, e.g. wait or log
    #     print(f"OpenAI API request exceeded rate limit: {e}")
    #     time.sleep(5)
    #     return get_chatgpt_response(message, model_type, chat_history=[])
    

    # try-error retry
    # timeout, 각각의 에러에 대해서 잡아야 함.