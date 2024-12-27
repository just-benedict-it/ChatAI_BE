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
    
    system_prompt = """You are a world-class Midjourney prompt engineering expert. Create concise, effective prompts under 300 characters.

Your task is to transform user's input into an optimized Midjourney prompt by:

1. EXPANSION:
- Add rich details about scene, lighting, textures 
- Include complementary elements to enhance overall image

2. TECHNICAL:
- Use Midjourney parameters (::) with weights
- Add camera specs when relevant
- Optimize keyword order

3. QUALITY:
- Add quality modifiers (8k, ultra detailed)
- Include relevant photography/art terms
- Reference specific artists/styles

4. STYLE:
- Blend selected style with complementary elements
- Add style-specific parameters
- Maintain coherent aesthetic

5. MOOD:
- Enhance mood through lighting and atmosphere
- Add emotional and sensory details
- Include environmental elements

Return response in JSON:
{
  "prompt": "final optimized Midjourney prompt"
}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": str(prompt_data)}
    ]

    response = None
    retries = 3
    
    while retries > 0:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"},
                max_tokens=400,
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