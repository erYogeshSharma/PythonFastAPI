import string
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from httpx import delete
from pydantic import BaseModel
from random import randrange
import psycopg2
# This is used to return the data in the form of dictionary
from psycopg2.extras import RealDictCursor

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi",
                                user="postgres", password='yogesh084', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as e:
        print('Database connection was unsuccessful!')
        print("error", e)
        time.sleep(2)

my_posts = [{'title': 'Post 1', 'content': 'This is a post', 'id': 1},
            {'title': 'Post 2', 'content': 'This is another post', 'id': 2}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Default value
    rating: Optional[int] = None  # Optional field


@app.get('/posts')  # Decorator
async def root():  # Name these function as descriptive as possible
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {'data': posts}


@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts(title, content,published) VALUES(%s,%s,%s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()  # commit the changes to db
    return {
        'data': new_post
    }


@app.get('/posts/{id}')
def get_post(id: int):  # automatically converts to int
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post with id ' + str(id) + ' not found')
    return {
        'data': post
    }


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post with id ' + str(id) + ' not found')


@app.put('/posts/{id}')
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id :{id} does not exists.")

    return {'data': updated_post}
