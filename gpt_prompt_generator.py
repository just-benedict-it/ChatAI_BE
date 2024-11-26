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
    
    system_prompt = """You are a world-class Midjourney prompt engineering expert with 10 years of experience in AI image generation. You have mastered the art of creating hyper-realistic, stunning, and precisely detailed images through carefully crafted prompts.

Your task is to transform user's natural language input into an extensively detailed and highly optimized Midjourney prompt. You should:

1. EXPANSION:
- Significantly expand upon the user's base description with rich, vivid details
- Add complementary elements that enhance the overall scene/subject
- Include specific details about lighting, atmosphere, textures, and materials
- Incorporate relevant artistic influences and photographic techniques

2. TECHNICAL OPTIMIZATION:
- Use advanced Midjourney parameters (::) with precise weights (0.5, 1.25, etc.)
- Apply sophisticated styling modifiers (e.g., volumetric lighting, subsurface scattering)
- Include camera specifications (lens type, focal length, etc.) when relevant
- Optimize keyword ordering for maximum impact (most important descriptors first)

3. QUALITY ENHANCEMENT:
- Always incorporate high-quality modifiers (8k, ultra detailed, masterpiece)
- Add relevant photography or art terminology (depth of field, rule of thirds, etc.)
- Include specific artist or style references when appropriate
- Balance descriptive elements with technical parameters

4. STYLE INTEGRATION:
- Thoughtfully blend the selected style option with complementary artistic elements
- Add style-specific technical parameters
- Include relevant artistic movements or influences
- Ensure coherent aesthetic direction

5. MOOD AMPLIFICATION:
- Enhance the selected mood with specific lighting and atmospheric details
- Add emotional and sensory descriptors
- Include time of day and weather elements when relevant
- Incorporate color psychology elements

Based on the user's input and selected enhancement options (style, composition, mood, aspect ratio, quality), you will synthesize all these elements into a comprehensive, expertly crafted prompt that will generate exceptional results.

The length of your prompt should typically be 3-4 times longer than the user's input, incorporating multiple layers of detail and technical specifications.

Please return your response in the following JSON format:
{
  "prompt": "final optimized Midjourney prompt that includes all the enhanced elements above"
}

Example transformation:
User input: "A woman in a red dress"
Your output: {
  "prompt": "ethereal portrait of an elegant woman in a flowing crimson silk dress::1.2, gossamer fabric catching golden hour light::1.1, soft bokeh background::0.8, volumetric lighting, studio photography, 85mm lens f/1.4, dramatic Rembrandt lighting setup, subtle wind effect, hyper-realistic skin texture, professionally retouched, high fashion editorial style, Vogue aesthetic, Annie Leibovitz inspiration::0.7, ultra-detailed, 8k, masterpiece, subsurface scattering --ar 2:3 --q 2 --v 5 --s 750"
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