from openai import OpenAI
from typing import Dict
from itertools import cycle
import json
import time
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
api_keys = [
    os.getenv("CHATGPT_API_1"),
    os.getenv("CHATGPT_API_2"),
    os.getenv("CHATGPT_API_3"),
]

# API 키 순환 설정
api_key_cycle = cycle(api_keys)

def get_next_api_key():
    return next(api_key_cycle)

async def get_midjourney_prompt(prompt_data: Dict):
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=get_next_api_key())
    
    system_prompt = """You are a 10-year experienced Midjourney prompt engineering expert.

Your task is to optimize user's natural language input into a highly effective Midjourney prompt. Based on the user's description and selected enhancement options (style, composition, mood, aspect ratio, quality), generate the most optimal prompt that will produce exceptional results in Midjourney.

While you should consider the provided options as guidelines, feel free to add or modify parameters and keywords to achieve the best possible outcome.

Please return your response in the following JSON format:
{
  "prompt": "final optimized Midjourney prompt"
}

Remember to incorporate advanced Midjourney techniques such as precise parameter weighting, optimal keyword ordering, and expert-level stylistic adjustments to ensure the highest quality image generation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": str(prompt_data)}
    ]

    response = None
    retries = 3
    
    while retries > 0:
        try:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"},
                max_tokens=1024
            )
            break
        except Exception as e:
            print(f'Error: {e}')
            print('Retrying...')
            retries -= 1
            time.sleep(2)

    if response:
        try:
            result = json.loads(response.choices[0].message.content)
            return result.get("prompt", "Error: Invalid response format")
        except json.JSONDecodeError:
            return "Error: Invalid JSON response"
    else:
        return "Error: Please try later"