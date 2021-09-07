from typing import List, Optional
from pydantic import BaseModel
from program.schemas.book import Book

class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    books: List[Book] = []

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None

class status(BaseModel):
    message: Optional[str] = None