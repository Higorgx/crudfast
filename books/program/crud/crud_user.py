from sqlalchemy.orm import Session
from program.model import users
from program.schemas import user
from sqlalchemy import update

hashpattern = "notreallyhashed"

def get_user(db: Session, user_id: int):
    return db.query(users.User).filter(users.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(users.User).filter(users.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(users.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user.UserCreate):
    fake_hashed_password = user.password + hashpattern
    db_user = users.User(email=user.email,username = user.username , hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def auth_user(db: Session, email: str, password: str):
    password += hashpattern
    user = get_user_by_email(db, email)
    return {"sucesso": user != None and user.hashed_password == password}
 
def update_user(db: Session, user: user.UserUpdate, user_id: int):
    db_user = update(users.User).where(users.User.id == user_id).values(**user.dict(exclude_unset=True))
    db.execute(db_user)
    db.commit()

def delete_user(db: Session, user_id: int):
    db_user = get_user(db=db, id=user_id)
    db.delete(db_user)
    db.commit()
