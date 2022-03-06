from pyexpat import model
from turtle import pos
from unittest import result
from app import oauth2
from .. import models,schemas, oauth2
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. database import engine, SessionLocal, get_db
from typing import Optional, List


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)




#@router.get("/", response_model=List[schemas.Post])
@router.get("/")
async def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int= 0, search:Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() ##To grab all the entries in the post table

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
    # (post.title,post.content,post.published)) ## Done to prevent SQL injections
    
    # new_post = cursor.fetchone()
    # conn.commit()

    #Efficient if the no. of columns in the table are less
    # new_post = models.Post(title=post.title, content= post.content, published=post.published)

    ## For tables having large no. of columns
    print(current_user.id)
    # print(current_user)
    new_post = models.Post(owner_id= current_user.id, **post.dict()) #This simply unpacks the dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post) ## Similar to RETURNING * feature in SQL 
    return new_post

## Extract a specific post
@router.get("/{id}",response_model=schemas.Post)  ##This id is the path parameter
async def get_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} was not found")
        

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()  ##Only required for write and delete options

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"The post with id: {id} does not exists")

    #To check if user wants to delete his own post or not
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) ##As sending a message in case after setting response to 204 will generate error

@router.put('/{id}', response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title,
    # post.content, post.published, (str(id))))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"The post with id: {id} does not exists")

    #To check if user wants to update his own post or not
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")

    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()


    return post_query.first()