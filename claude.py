from dotenv import load_dotenv
import os
import time
import anthropic

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

async def get_claude_response(message, model_type, chat_history=[]):
    api_key = ANTHROPIC_API_KEY

    client = anthropic.AsyncAnthropic(
        api_key=api_key
    )

    if model_type == 1:
        model = "claude-3-5-sonnet-20240620"
    elif model_type == 2:
        model = "claude-3-haiku-20240307"
    else:
        model = None

    # chat_history를 messages 배열로 변환하면서 연속된 역할을 방지
    messages = []
    prev_role = None
    for chat in chat_history:
        role = "assistant" if chat.type == 0 else "user"
        if role != prev_role:
            messages.append({"role": role, "content": chat.message})
            prev_role = role
        else:
            # 연속된 역할이 나타나면 이전 메시지에 내용을 추가
            messages[-1]["content"] += "\n" + chat.message

    # 새로운 사용자 메시지 추가
    if not messages or messages[-1]["role"] != "user":
        messages.append({"role": "user", "content": message})
    else:
        # 마지막 메시지가 이미 사용자 메시지라면 내용을 추가
        messages[-1]["content"] += "\n" + message

    message = None
    try:
        message = await client.messages.create(
            model=model,
            max_tokens=1000,
            messages=messages,
            system="Please produce an answer within 500 characters"
        ) 
    except Exception as e:    
        print(e)   

    if message:
        print("used model : ", model)
        print(message.content)
        print(message.content[0].text)
        return message.content[0].text
    else: 
        return "Please try later"