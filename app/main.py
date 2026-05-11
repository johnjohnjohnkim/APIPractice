from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional
import time

import psycopg
from psycopg.rows import dict_row 

from . import models
from .database import engine, SessionLocal

models.Base.metadata.createl_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #defaults to True
    rating: Optional[int] = None

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
@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(posts: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                        (posts.title, posts.content, posts.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}

# title str, content str, category, Bool published
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    postid = cursor.fetchone()
    if not postid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found")
    return {"post_detail": postid}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    cursor.execute(f"""DELETE FROM posts WHERE id = {id} RETURNING *""")
    deletePost = cursor.fetchone()
    conn.commit()

    if deletePost == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(f"""UPDATE posts SET title = %s, content = %s, published = %s   WHERE id = {id} RETURNING *""", (post.title, post.content, post.published))
    updatedPost = cursor.fetchone()
    conn.commit()

    if updatedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {id} was not found")

    return {"data": updatedPost}
