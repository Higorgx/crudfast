from typing import List
from fastapi import Depends, HTTPException, FastAPI, Body
from program.crud import crud_user, crud_book
from program.schemas import book, user
from sqlalchemy.orm import Session
from program.db.database import SessionLocal
from program.routes.api import app


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", tags=["Books"], response_model=List[book.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    book = crud_book.get_books(db, skip=skip, limit=limit)
    return book

@app.get("/book/{book_id}", tags=["Books"], response_model=book.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud_book.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="book not found")
    return db_book

@app.post("/books/{user_id}/book/", tags=["Books"], response_model=book.Book)
def create_book_for_user(
    user_id: int, book: book.bookCreate, db: Session = Depends(get_db)
):
    return crud_book.create_user_book(db=db, book=book, user_id=user_id)

@app.put("/book/update/{book_id}", tags=["Books"], response_model=book.BookUpdate)
def update_book(book_id: int, book: book.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud_book.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail="book not found")
    return crud_book.update_book(book_id=book_id, book = book, db=db)
    

@app.delete("/book/delete/{book_id}", tags=["Books"], response_model=book.status)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud_book.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail="Couldn't delete the book!")
    db_book = crud_book.delete_book(db, book_id=book_id)
    return book.status(message="book was successfully deleted!")
