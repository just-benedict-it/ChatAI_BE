
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, func,or_, asc, desc,case
from datetime import datetime, timedelta
import uuid
import schemas
import models
from database import engine, SessionLocal
from fastapi.responses import HTMLResponse
from chatgpt import get_chatgpt_response
from dotenv import load_dotenv
import os
import openai
import time

load_dotenv()
openai.api_key = os.getenv("CHATGPT_API")

app = FastAPI(debug=True)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "hello"

# 유저 생성 (최초 1회)
@app.post("/user/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_id = str(uuid.uuid4())
    new_profile = models.User(id=user_id, **user.dict())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {
        "user_id": new_profile.id,
    }

# 유저 접속 기록 (매일 최초 1회)
@app.post("/create_user_activity/", response_model=schemas.UserActivityRead)
def create_user_activity(activity: schemas.UserActivityCreate, db: Session = Depends(get_db)):
    new_activity = models.UserActivity(**activity.dict())
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity


# 채팅방 기록 불러오기
@app.get("/chat_list/{user_id}")
def get_user_chat_list(user_id: str, db: Session = Depends(get_db)):
    chats = (db.query(models.ChatList)
             .filter(models.ChatList.user_id == user_id)
             .filter(models.ChatList.is_del == False)
             .order_by(
                 desc(models.ChatList.favorite),  # 1. favorite=true인 것들 먼저
                 asc(models.ChatList.favorite_order),  # 2. 그 중에서도 favorite_order가 높은 순서대로
                 desc(models.ChatList.created_at)  # 3. 그 다음엔 favorite=false인 것들, 날짜순서대로
             )
             .all())
    return chats

# 채팅방 생성
@app.post("/chat_list/")
async def create_chat_list(chat: schemas.ChatListCreate, db: Session = Depends(get_db)):
    chat_id = str(uuid.uuid4())
    chat_list = models.ChatList(chat_id=chat_id, **chat.dict())
    db.add(chat_list)
    db.commit()
    db.refresh(chat_list)
    return {
    "chat_id": chat_list.chat_id
    }

# 채팅방 이름 변경
@app.put("/chat/rename/")
def rename_chat(chat_id: str, new_chat_name: str,db: Session = Depends(get_db)):
    chat = db.query(models.ChatList).filter(models.ChatList.chat_id == chat_id).first()
    if chat:
        chat.chat_name = new_chat_name
        db.commit()
        db.close()
        return {"message": "Chat name updated successfully"}
    db.close()
    raise HTTPException(status_code=404, detail="Chat not found")

# 채팅방 상단 고정
@app.put("/chat/favorite")
def favorite_chat(user_id: str, chat_id: str, db: Session = Depends(get_db)):
    chat = db.query(models.ChatList).filter(
        models.ChatList.chat_id == chat_id).first()

    if chat:
        if chat.favorite:
            # 대화창이 이미 고정된 상태라면 고정 해제
            chat.favorite = False
            chat.favorite_order = None  # 고정 순서를 None으로 설정
            message = "Unmarked as favorite successfully"
        else:
            # 대화창을 고정하기 위해 가장 높은 favorite_order 값 찾기
            max_favorite_order = db.query(func.max(models.ChatList.favorite_order)).filter(
                models.ChatList.user_id == user_id).scalar()
            if max_favorite_order is None:
                max_favorite_order = 0
            
            # 기존에 고정된 대화들의 순서를 1씩 증가시키기
            chats_to_update = db.query(models.ChatList).filter(
                models.ChatList.user_id == user_id, models.ChatList.favorite_order <= max_favorite_order).all()
            for c in chats_to_update:
                c.favorite_order += 1

            # 대화창을 맨 위로 고정
            chat.favorite = True
            chat.favorite_order = 1
            message = "Marked as favorite successfully"

        db.commit()
        db.close()
        return {"message": message}

    db.close()
    raise HTTPException(status_code=404, detail="Chat not found")

# 채팅방 삭제
@app.put("/chat/delete")
def delete_chat(chat_id: str,db: Session = Depends(get_db)):
    chat = db.query(models.ChatList).filter(models.ChatList.chat_id == chat_id).first()
    if chat:
        chat.is_del = True
        db.commit()
        db.close()
        return {"message": "Updated is_del successfully"}
    db.close()
    raise HTTPException(status_code=404, detail="Chat not found")

# 채팅 기록 불러오기
@app.get("/chats/{chat_id}")
def get_chat_history_by_chatId(chat_id: str, db: Session = Depends(get_db)):
    chat_history = db.query(models.ChatHistory).filter(models.ChatHistory.chat_id == chat_id).all()

    # chat_history를 원하는 형식으로 변환
    formatted_chat_history = []
    for chat in chat_history:
        formatted_chat = {
            "id": chat.id,
            "sender": 'bot' if chat.type == 0 else 'user',
            "content": chat.message,
            "created_at" : chat.created_at
        }
        formatted_chat_history.append(formatted_chat)

    return formatted_chat_history

# 무료 채팅 개수 불러오기
@app.get("/free_message/{user_id}")
def get_free_message(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"free_message": user.free_message}

# 무료 채팅 개수 업데이트
@app.post("/user/update_free_message/{user_id}")
def update_free_message(user_id: str, free_message: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.free_message += free_message
    db.commit()
    
    return {"message": "Free messages updated successfully."}


# 채팅 전송
@app.post("/chat/send")
async def send_chat(chat: schemas.ChatHistoryCreate, model_type:int, subscribed:schemas.Subscribed, db: Session = Depends(get_db)):
    start_time = time.time()
    user = db.query(models.User).filter(models.User.id == chat.user_id).first()
    
    # 사용자가 존재하지 않는 경우, 특정 응답 반환
    if not user:
        # 사용자가 존재하지 않는 경우 에러 로깅 및 저장
        error_message = "User not found"
        save_chat(db, error_message, error_message, type=4, message=error_message)
        return {
            "ai_response": "An error has occurred. Please close the app and try again!",
            "free_message": 0  # 사용자가 없으므로 free_message는 0으로 설정
        }

    # free_message 값 확인
    if not subscribed.subscribed and user.free_message <= 0:
        return {
            "ai_response": "Free Message has been used up!",
            "free_message": user.free_message
        }
  
    
    message = chat.message  # 요청 바디에서 message를 추출
    # chat history 불러오기
    chat_history = get_chat_history(chat.chat_id, db)
    # GPT로부터 응답 받기
    ai_response =  await get_chatgpt_response(message,model_type,chat_history)

    # GPT로부터 응답 받기
    # 사용자 채팅 저장
    try:
        save_chat(db, chat.user_id, chat.chat_id, type=1, message=message)
    except Exception as e:
        error_message = "Error Saving User Chat"
        save_chat(db, error_message, error_message, type=2, message=e)

        print(f"An error occurred: {e}")

    # GPT 채팅 저장
    try:
        save_chat(db, chat.user_id, chat.chat_id, type=0, message=ai_response)
    except Exception as e:
        error_message = "Error Saving Bot Chat"
        save_chat(db, error_message, error_message, type=3, message=e)
        print(f"An error occurred: {e}")


    # free_message 값을 1 감소시키기
    if user : 
        user.free_message -= 1
    db.commit()
    end_time = time.time()

    print("총 실행 시간:", end_time - start_time, "초")
    # 채팅 전송 결과 반환
    return {
        "ai_response": ai_response,
        "free_message" : user.free_message
    }
    
# 채팅 전송
@app.post("/chat/initialChat")
async def seva_initial_chat(chat: schemas.ChatHistoryCreate, db: Session = Depends(get_db)):
    # 초기 채팅 저장
    save_chat(db, chat.user_id, chat.chat_id, type=0, message=chat.message)
    db.commit()



# 구매 현황 업데이트
@app.post("/subscription_status/update/")
async def update_subscription_status(store_log: schemas.StoreLogCreate, db: Session = Depends(get_db)):
    # StoreLog에 새로운 레코드 추가
    new_log = models.StoreLog(**store_log.dict())
    db.add(new_log)
    
    # # type에 따른 구독 일자 설정
    # if store_log.type == 1:
    #     subscription_days = 0
    # elif store_log.type == 2:
    #     subscription_days = 30
    # elif store_log.type == 3:
    #     subscription_days = 365
    # else:
    #     raise HTTPException(status_code=400, detail="Invalid subscription type")
    
    # # 해당 사용자의 SubscriptionStatus 조회
    # subscription_status = db.query(models.SubscriptionStatus).filter(models.SubscriptionStatus.user_id == store_log.user_id).first()
    
    # # 사용자의 SubscriptionStatus가 없는 경우 새로 생성
    # if not subscription_status:
    #     subscription_status = models.SubscriptionStatus(user_id=store_log.user_id, subscribed=True, expiry_date=datetime.utcnow() + timedelta(days=subscription_days))
    #     db.add(subscription_status)
    # else:
    #     # 이미 구독 중인 경우 expiry_date 업데이트
    #     subscription_status.expiry_date += timedelta(days=subscription_days)
    
    db.commit()

    return {"message": "Subscription status updated successfully"}

# 구매 현황 확인하기 (백그라운드)
@app.post("/subscription_status/validate/")
def update_subscription_status_daily(db: Session = Depends(get_db)):
    # 현재 시각을 기준으로 expiry_date가 지난 사용자 조회
    expired_users = db.query(models.SubscriptionStatus).filter(models.SubscriptionStatus.expiry_date < datetime.utcnow()).all()

    for user in expired_users:
        user.subscribed = False

    db.commit()

    return {"message": "Subscription status validated successfully"}

# 구독 여부 확인 (유저별로)
@app.get("/subscribed_status/{user_id}")
def get_subscribed_status(user_id: str):
    db_session = SessionLocal()
    try:
        subscription_status = db_session.query(models.SubscriptionStatus).filter(models.SubscriptionStatus.user_id == user_id).first()
        if not subscription_status:
            raise HTTPException(status_code=404, detail="User not found")
        return {"subscribed": subscription_status.subscribed}
    finally:
        db_session.close()


# 지난 N개의 chat_history를 불러오는 함수
def get_chat_history(chat_id: str, db: Session, n:int = 6):
    return db.query(models.ChatHistory).filter(models.ChatHistory.chat_id == chat_id).order_by(models.ChatHistory.created_at.desc()).limit(n).all()

# # 채팅 데이터를 저장하는 함수
# def save_chat(db: Session, user_id: str, chat_id : str,type:int,message: str):
#     chat = models.ChatHistory(chat_id=chat_id, user_id=user_id, type=type,  created_at=datetime.now() + timedelta(hours=9), message=message)
#     db.add(chat)
#     db.commit()
#     db.refresh(chat)
#     return chat

from sqlalchemy.exc import SQLAlchemyError

def save_chat(db: Session, user_id: str, chat_id: str, type: int, message: str):
    try:
        # 채팅 정보를 생성하고 데이터베이스에 추가
        chat = models.ChatHistory(chat_id=chat_id, user_id=user_id, type=type, created_at=datetime.now() + timedelta(hours=9), message=message)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat
    except SQLAlchemyError as e:
        # 오류 발생 시, 데이터베이스 세션 롤백
        db.rollback()
        print(f"An error occurred while saving chat: {e}")  # 로깅을 위해 오류 메시지 출력
        # 여기서 오류를 기록하거나 추가 조치를 취할 수 있습니다. 예를 들어, 오류를 로깅하거나 특정 조건에 따라 재시도할 수 있습니다.
        return None  # 채팅 저장 실패를 나타내는 None 반환

# 유저 접속 기록 (매일 최초 1회)
@app.post("/ad_log/")
def create_ad_log(ad_log: schemas.AdLogCreate, db: Session = Depends(get_db)):
    new_ad_log = models.AdLog(**ad_log.dict())
    db.add(new_ad_log)
    db.commit()
    db.refresh(new_ad_log)
    return new_ad_log

# 에러 로그 
@app.post("/error_log/")
def create_error_log(error_log: schemas.ErrorLogCreate, db: Session = Depends(get_db)):
    new_error_log = models.ErrorLog(**error_log.dict())
    db.add(new_error_log)
    db.commit()
    db.refresh(new_error_log)
    return new_error_log


@app.get("/users/")
async def get_all_profiles(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/chat")
def get_all_chat_history(db: Session = Depends(get_db)):
    return db.query(models.ChatHistory).all()

@app.get("/chat_list")
def get_all_chat_list(db: Session = Depends(get_db)):
    return db.query(models.ChatList).all()

@app.get("/get_all_user_activities/")
def get_all_user_activities(db: Session = Depends(get_db)):
    return db.query(models.UserActivity).all()

@app.get("/get_all_subscription_status/")
def get_all_subscription_status(db: Session = Depends(get_db)):
    return db.query(models.SubscriptionStatus).all()


# if __name__ == "__main__":
#     import uvicorn
#     # 나중에 host 부분 변경 필요
#     # uvicorn.run("main:app", host="10.182.0.2", port=8000, reload=True)
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
