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
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=message,
            size="1024x1024",
            # size="256x256",
            quality="standard",
            n=1,
        )
    except Exception as e:    
        print(e)   
    if response:
        return response.data[0].url
    else: 
        return "Please try again"
