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


@app.post("/users/", tags=["Users"], response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)

@app.post("/user/auth", tags=["Users"])
def auth_user(email: str, password: str, db: Session = Depends(get_db)):
    return crud_user.auth_user(db, email=email, password=password)

@app.get("/users/", tags=["Users"], response_model=List[user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", tags=["Users"] , response_model=user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/user/update/{user_id}", tags=["Users"], response_model=user.status)
def update_user(user_id: int, items: user.UserUpdate = Body(..., embed=True), db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_id(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    crud_user.update_user(user_id=user_id, user=items, db=db)
    return user.status(message="User updated successfully")

@app.delete("/user/delete/{user_id}", tags=["Users"], response_model=user.status)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="Couldn't delete the user!")
    db_user = crud_user.delete_user(db, user_id=user_id)
    return user.status(message="User was successfully deleted!")
