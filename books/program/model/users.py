from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from program.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    books = relationship("Book", back_populates="owner", cascade="all, delete")