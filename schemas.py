

from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    os: str
    country: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: str
    date_joined: datetime

class UserUpdate(BaseModel):
    os: Optional[str] = None
    country: Optional[str] = None
    free_message: Optional[int] = None
    used_message: Optional[int] = None
    subscribed: Optional[bool] = None
    is_test: Optional[bool] = None
    experiment: Optional[bool] = None

# ChatList Schemas
class ChatListBase(BaseModel):
    user_id: str
    chat_name : str
    img_url : Optional[str] = None


class ChatListCreate(ChatListBase):
    pass

class ChatListRead(ChatListBase):
    id: int
    chat_id : str
    created_at: datetime
    favorite_order : int
    favorite : bool
    is_del : bool


# ChatHistory Schemas
class ChatHistoryBase(BaseModel):
    chat_id: str
    user_id: str
    type: int
    message: str

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistoryRead(ChatHistoryBase):
    id: int
    created_at: datetime



# StoreLog Schemas
class StoreLogBase(BaseModel):
    user_id: str
    type : str
    price: int
    currency: str

class StoreLogCreate(StoreLogBase):
    pass

class StoreLogRead(StoreLogBase):
    id: int
    created_at: datetime

# UserActivity Schemas
class UserActivityBase(BaseModel):
    activity_type: int
    user_id: str
    activity_action: Optional[int] = None

class UserActivityCreate(UserActivityBase):
    pass

class UserActivityRead(UserActivityBase):
    id: int
    created_at: datetime

class Subscribed(BaseModel):
    subscribed : bool

class AdLogBase(BaseModel):
    user_id: str
    

class AdLogCreate(AdLogBase):
    pass

class ErrorLogBase(BaseModel):
    error_message: str


class ErrorLogCreate(ErrorLogBase):
    pass

class InitialPrompt(BaseModel):
    role: str
    content: str
    
class ChatBotCardBase(BaseModel):
    chatbotcard: str
    user_id: str

class ChatBotCardCreate(ChatBotCardBase):
    pass


class DalleImageLogBase(BaseModel):
    user_id: str
    message: str
class DalleImageLogCreate(BaseModel):
    pass