import program
from fastapi import FastAPI
from program.model import users, books
from program.db.database import engine
from program.routes.users import *
from program.routes.books import *


books.Base.metadata.create_all(bind=engine)
users.Base.metadata.create_all(bind=engine)
