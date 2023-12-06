

from pydantic import BaseModel, validator
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    os: str
    country: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: str
    date_joined: datetime

# ChatList Schemas
class ChatListBase(BaseModel):
    user_id: str
    chat_name : str


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