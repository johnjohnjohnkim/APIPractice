from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #defaults to True

class CreatePost(PostBase):
    pass
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool
#     id: int
#     created_at: datetime

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
