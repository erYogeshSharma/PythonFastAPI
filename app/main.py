
import re
from turtle import pos
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{'title': 'Post 1', 'content': 'This is a post', 'id': 1},
            {'title': 'Post 2', 'content': 'This is another post', 'id': 2}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # Default value
    rating: Optional[int] = None  # Optional field


def find_post(id):
    print('input', id)
    for post in my_posts:
        print(post['id'])
        if post['id'] == id:
            return post
    return None


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get('/posts')  # Decorator
async def root():  # Name these function as descriptive as possible
    return {'data': my_posts}


@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {
        'data': my_posts
    }


@app.get('/posts/{id}')
def get_post(id: int, response: Response):  # automatically converts to int
    post = find_post(id)
    if post is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     'data': 'Post with id ' + str(id) + ' not found'
        # }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post with id ' + str(id) + ' not found')
    return {
        'data': post
    }


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post with id ' + str(id) + ' not found')
    my_posts.pop(index)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id :{id} does not exists.")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}
