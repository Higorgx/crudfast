from typing import Optional
from pydantic import BaseModel


class bookBase(BaseModel):
    title: str
    description: Optional[str] = None


class bookCreate(bookBase):
    pass


class Book(bookBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
        
class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class status(BaseModel):
    message: Optional[str] = None