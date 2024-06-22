
from typing import List
from fastapi import Depends, FastAPI,  status, HTTPException
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi",
#                                 user="postgres", password='yogesh084', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful!')
#         break
#     except Exception as e:
#         print('Database connection was unsuccessful!')
#         print("error", e)
#         time.sleep(2)

# my_posts = [{'title': 'Post 1', 'content': 'This is a post', 'id': 1},
#             {'title': 'Post 2', 'content': 'This is another post', 'id': 2}]


@app.get('/posts', response_model=List[schemas.Post])  # Decorator
# Name these function as descriptive as possible
async def root(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post('/createposts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title, content,published) VALUES(%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()  # commit the changes to db

    # **post.model_dump() unpacks the dictionary
    new_post = models.Post(**post.model_dump())  # create a new post
    db.add(new_post)     # add the new post to the database
    db.commit()          # commit the changes to db
    db.refresh(new_post)  # retrieve the newly created post from the database
    return new_post


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):  # automatically converts to int
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post with id ' + str(id) + ' not found')
    return post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post with id ' + str(id) + ' not found')

    post.delete(synchronize_session=False)
    db.commit()


@ app.put('/posts/{id}', response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id :{id} does not exists.")

    post_query.update(update_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
