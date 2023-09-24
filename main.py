from fastapi import FastAPI, HTTPException, Request,Depends
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, select
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from fastapi.middleware.cors import CORSMiddleware
from chatgpt import get_chatgpt_response
from sqlalchemy.orm import sessionmaker, Session,aliased,joinedload
import models, schemas, database
from database import engine, SessionLocal
from datetime import timedelta
from datetime import datetime
import threading, os 
from urllib.parse import urlparse
import uuid


app = FastAPI(debug=True)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "hello"

# user_id 생성
@app.post("/user/")
async def create_profile(os, device_id, db: Session = Depends(get_db)):
    user_id = generate_unique_key()
    new_profile = models.User(id=user_id, os=os, device_id=device_id)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {
        "user_id": new_profile.id,
    }

@app.get("/generate_unique_key")
def generate_unique_key():
    unique_key = str(uuid.uuid4())
    return unique_key

# chat_id 생성
@app.post("/chat")
async def create_chat_id():
    chat_id = generate_unique_key()
    return {
        "chat_id": chat_id,
    }

class ChatInput(BaseModel):
    message: str

# chat 생성
@app.post("/chats/{user_id}/{chat_id}")
async def send_chat(chat_id: str, user_id: str, chat_input: ChatInput, db: Session = Depends(get_db)):
    message = chat_input.message  # 요청 바디에서 message를 추출

    # chat history 불러오기
    chat_history = get_chat_history(chat_id, db)

    # GPT로부터 응답 받기
    ai_response = get_chatgpt_response(message, chat_history) 

    # 사용자 채팅 저장
    save_chat(db, user_id, chat_id, type=1, message=message)
    # GPT 채팅 저장
    save_chat(db, user_id, chat_id, type=0, message=ai_response)

    # 채팅 전송 결과 반환
    return {
        "ai_response": ai_response,
    }

# chat_history를 불러오는 함수
# def get_chat_history(chat_id: str, db: Session = Depends(get_db)):
#     return db.query(models.ChatHistory).filter(models.ChatHistory.chat_id == chat_id).order_by(models.ChatHistory.created_at).all()

# 지난 N개의 chat_history를 불러오는 함수
def get_chat_history(chat_id: str, db: Session, n:int = 6):
    return db.query(models.ChatHistory).filter(models.ChatHistory.chat_id == chat_id).order_by(models.ChatHistory.created_at.desc()).limit(n).all()


@app.get("/chats/{chat_id}")
def get_chat_history_by_chatId(chat_id: str, db: Session = Depends(get_db)):
    chat_history = db.query(models.ChatHistory).filter(models.ChatHistory.chat_id == chat_id).all()

    # chat_history를 원하는 형식으로 변환
    formatted_chat_history = []
    for chat in chat_history:
        formatted_chat = {
            "id": chat.id,
            "sender": 'bot' if chat.type == 0 else 'user',
            "content": chat.message
        }
        formatted_chat_history.append(formatted_chat)

    return formatted_chat_history

# 채팅 데이터를 저장하는 함수
def save_chat(db: Session, user_id: str, chat_id : str,type:int,message: str):
    chat = models.ChatHistory(chat_id=chat_id, user_id=user_id, type=type,  created_at=datetime.now() + timedelta(hours=9), message=message)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

@app.post("/chat_list")
def create_chat_list(user_id: str, chat_id:str, db: Session = Depends(get_db)):
    try:
        chat = models.ChatList(chat_id=chat_id, user_id=user_id)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat.chat_id
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating chat")
    finally:
        db.close()

# 모든 chat_history를 불러오는 함수
@app.get("/chat_list/{user_id}")
def get_user_chat_list(user_id: str, db: Session = Depends(get_db)):
    return db.query(models.ChatList).filter(models.ChatList.user_id == user_id).all()



# 모든 User 프로필 조회
@app.get("/users/")
async def get_profiles(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# 모든 chat_history를 불러오는 함수
@app.get("/chat")
def get_all_chat_history( db: Session = Depends(get_db)):
    return db.query(models.ChatHistory).all()

# 모든 chat_history를 불러오는 함수
@app.get("/chat_list")
def get_all_chat_list( db: Session = Depends(get_db)):
    return db.query(models.ChatList).all()

@app.post("/create_user_activity/")
def create_user_activity(activity_type:int, user_id:str,db: Session = Depends(get_db)):
    new_activity = models.UserActivity(activity_type=activity_type,user_id=user_id)
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

@app.get("/get_all_user_activities/")
def get_all_user_activities(db: Session = Depends(get_db)):
    activities = db.query(models.UserActivity).all()
    return activities

if __name__ == "__main__":
    import uvicorn
    # 나중에 host 부분 변경 필요
    # uvicorn.run("main:app", host="10.182.0.2", port=8000, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
