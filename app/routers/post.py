from .. import models, schemas
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)


@router.get("/")
def read_root():
    return {"Hello":"World"}

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@router.get("", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(posts: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                     (posts.title, posts.content, posts.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostBase)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    postid = db.query(models.Post).filter(models.Post.id == id).first()

    if not postid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found")
    return postid

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute(f"""DELETE FROM posts WHERE id = {id} RETURNING *""")
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found")
    
    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute(f"""UPDATE posts SET title = %s, content = %s, published = %s   WHERE id = {id} RETURNING *""", (post.title, post.content, post.published))
    # updatedPost = cursor.fetchone()
    # conn.commit()

    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {id} was not found")
    
    query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return query.first()