from database import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id = Column(String(100), primary_key=True, index=True)  # 아이디는 100자로 제한
    date_joined = Column(DateTime, default=datetime.utcnow)
    os = Column(String(50))  # OS 이름은 50자로 제한
    country = Column(String(50))  # 국가 이름은 50자로 제한
    free_message = Column(Integer, default=5)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(String(100), index=True)  # 채팅 아이디는 100자로 제한
    user_id = Column(String(100), index=True)
    type = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    message = Column(String(1000))  # 메시지는 1000자로 제한
    
class ChatList(Base):
    __tablename__ = "chat_list"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(String(100), index=True)
    user_id = Column(String(100), index=True)
    chat_name = Column(String(100), index=True)
    favorite = Column(Boolean, default=False, index=True)
    favorite_order = Column(Integer, autoincrement=True)
    is_del = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class StoreLog(Base):
    __tablename__ = "store_log"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), index=True)
    type = Column(String(50), index=True)
    price = Column(Integer)
    currency = Column(String(10))  # 통화 코드는 10자로 제한 (예: USD, KRW)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserActivity(Base):
    __tablename__ = "user_activity"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    activity_type = Column(Integer, index=True)
    user_id = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SubscriptionStatus(Base):
    __tablename__ = "subscription_status"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), index=True)
    subscribed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)