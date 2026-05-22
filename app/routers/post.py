from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)


@router.get("", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    print(curr_user.email)
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(posts: schemas.CreatePost, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                     (posts.title, posts.content, posts.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(curr_user.id)
    new_post = models.Post(user_id = curr_user.id, **posts.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    print(curr_user.email)
    # cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    postid = db.query(models.Post).filter(models.Post.id == id).first()

    if not postid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found")
    return postid

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(f"""DELETE FROM posts WHERE id = {id} RETURNING *""")
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} was not found")
    
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")
    
    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(f"""UPDATE posts SET title = %s, content = %s, published = %s   WHERE id = {id} RETURNING *""", (post.title, post.content, post.published))
    # updatedPost = cursor.fetchone()
    # conn.commit()
    
    print(curr_user.email)

    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post {id} was not found")
    
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action!")

    
    query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return query.first()