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


    # chat_history를 messages 배열에 추가
    messages = [{"role": "assistant" if chat.type == 0 else "user", "content": chat.message} for chat in chat_history]
    messages.append({"role": "user", "content": message})


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
