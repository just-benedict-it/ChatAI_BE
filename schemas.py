from pydantic import BaseModel,validator
from datetime import datetime

class User(BaseModel):
    id: str
    date_joined: datetime
    os: str
    country : str
    class Config:
        orm_mode = True

class ChatHistory(BaseModel):
    id: int
    chat_id : str
    user_id: int
    type: int
    created_at: datetime
    message : str
    class Config:
        orm_mode = True

class ChatList(BaseModel):
    id: int
    chat_id : str
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class StoreLog(BaseModel):
    id: int
    user_id: int
    platform: int
    type : int
    price : int
    currency : int
    created_at: datetime
    class Config:
        orm_mode = True

class UserActivity(BaseModel):
    id: int
    activity_type: int
    user_id: str
    created_at: datetime
    class Config:
        orm_mode = True



# class UserActivityCreate(BaseModel):
#     activity_type: int
#     user_id: str
    

# class UserActivityInDB(UserActivityCreate):
#     id: int
#     created_at: datetime

#     class Config:
#         orm_mode = True


# class UserActivityInput(BaseModel):
#     activity_type: int
#     user_id: int