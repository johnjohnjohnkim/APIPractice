from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional, List
import time
from sqlalchemy.orm import Session

from . import utils

import psycopg
from psycopg.rows import dict_row 

from . import models, schemas
from .database import engine, get_db

from .routers import post, user, authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg.connect(host = 'localhost', dbname = 'fastapi', user = 'postgres', password = 'password', row_factory=dict_row)
        cursor = conn.cursor()

        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("error: ", error)
        time.sleep(2)

#Path Operation

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)