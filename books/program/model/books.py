from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from program.db.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True,  index=True )
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="books")