from database import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True, index=True)
    date_joined = Column(DateTime,default=datetime.utcnow)
    os = Column(String)
    country = Column(String)
    free_message = Column(Integer, default=5)

# 대화 데이터
class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(String, index=True)
    user_id = Column(String, index=True)
    # ai : 0 / user : 1 / love_score : 2
    type = Column(Integer, index=True)
    created_at = Column(DateTime,default=datetime.utcnow)
    message = Column(String)
    
class ChatList(Base):
    __tablename__ = "chat_list"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(String, index=True)
    user_id = Column(String, index=True)
    chat_name = Column(String, index=True)
    favorite = Column(Boolean, default=False,index=True)
    favorite_order = Column(Integer, autoincrement=True)
    is_del = Column(Boolean, default=False,index=True)
    created_at = Column(DateTime,default=datetime.utcnow)



# 구매 데이터
class StoreLog(Base):
    __tablename__ = "store_log"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, index=True)
    platform = Column(String)
    # 1번 구독 : 1, 2번 구독 : 2
    type = Column(Integer, index=True)
    price = Column(Integer)
    currency = Column(String)
    created_at = Column(DateTime,default=datetime.utcnow)

# 유저 활동 로그
class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    activity_type = Column(Integer, index=True)
    user_id = Column(String, index=True)
    created_at = Column(DateTime,default=datetime.utcnow)

# 구독 여부 확인
class SubscriptionStatus(Base):
    __tablename__ = "subscription_status"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String,index=True)
    subscribed = Column(Boolean, default=False)
    # 생성일자를 기록하기 위한 열
    created_at = Column(DateTime, default=datetime.utcnow)
    # 구독 만료 날짜를 나타내는 열
    expiry_date = Column(DateTime)  