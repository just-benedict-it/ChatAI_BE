from dotenv import load_dotenv
import os
from itertools import cycle
import time
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("DALLE_API")

async def get_dalle_response(message):
    # openai 라이브러리에 API 키 설정
    client = OpenAI(api_key=API_KEY)

    response = None
    retries = 3    
    while retries > 0: 
        try:
            response = client.images.generate(
                model="dall-e-2",
                prompt=message,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            break  # 성공적으로 응답을 받았으므로 반복문 탈출
        except Exception as e:    
            print(e)   
            print('Timeout error, retrying...')    
            retries -= 1    
            time.sleep(2)    

    if response:
        return response.data[0].url
    else: 
        return "Please try again"
