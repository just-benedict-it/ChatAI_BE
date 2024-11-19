from database import Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from datetime import datetime,timedelta
from sqlalchemy import func

class User(Base):
    __tablename__ = "user"
    id = Column(String(100), primary_key=True, index=True)  # 아이디는 100자로 제한
    date_joined = Column(DateTime, default=datetime.utcnow)
    os = Column(String(50))  # OS 이름은 50자로 제한
    country = Column(String(50))  # 국가 이름은 50자로 제한
    free_message = Column(Integer, default=3)
    used_message = Column(Integer, default=0)
    subscribed = Column(Boolean, default=False, index=True)
    is_test = Column(Boolean, default=False, index=True)
    experiment = Column(Boolean, default=False, index=True)
    app = Column(String(50))

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(String(100), index=True)  # 채팅 아이디는 100자로 제한
    user_id = Column(String(100), index=True)
    type = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    message = Column(String(10000))  # 메시지는 1000자로 제한
    
class ChatList(Base):
    __tablename__ = "chat_list"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(String(100), index=True)
    user_id = Column(String(100), index=True)
    chat_name = Column(String(100), index=True)
    favorite = Column(Boolean, default=False, index=True)
    favorite_order = Column(Integer, autoincrement=True, index=True)
    is_del = Column(Boolean, default=False, index=True)
    img_url = Column(String(255), index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        Index('idx_chat_list_user_id_is_del', 'user_id', 'is_del'),
        Index('idx_chat_list_favorite_order', 'favorite', 'favorite_order', 'created_at'),
    )
    

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
    activity_action = Column(Integer, index=True)
    user_id = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SubscriptionStatus(Base):
    __tablename__ = "subscription_status"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), index=True)
    subscribed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)

class AdLog(Base):
    __tablename__ = "ad_log"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ErrorLog(Base):
    __tablename__ = "error_log"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    error_message = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class ChatBotCardLog(Base):
    __tablename__ = "chatbotcard_log"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), index=True)
    chatbotcard = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DalleImageLog(Base):
    __tablename__ = "dalle_image_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), index=True)
    message = Column(String(10000))  # 메시지는 1000자로 제한
    created_at = Column(DateTime, default=datetime.utcnow)
