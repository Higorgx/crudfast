from sqlalchemy.orm import Session
from program.model import books
from program.schemas import book
from sqlalchemy import update


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(books.Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(books.Book).filter(books.Book.id == book_id).first()


def create_user_book(db: Session, book: book.bookCreate, user_id: int):
    db_book = books.Book(**book.dict(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, request_body: book.BookUpdate, id: int):
    book = get_book(db, id)
    if book != None:
        db_book_update = update(books.Book).where(books.Book.id == id).values(
            title=request_body.title, description=request_body.description
        )
        print(db_book_update)
        db.execute(db_book_update)
        db.commit()
        return True
    return False

def delete_book(db: Session, book_id: int):
    db_book = get_book(db=db, book_id=book_id)
    db.delete(db_book)
    db.commit()
