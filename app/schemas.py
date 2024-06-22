
from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:  # This is a class that is used to configure the Pydantic model
        orm_mode = True
    # This tells Pydantic to serialize the data to ensure that it can be read by the ORM
    # This is necessary because the ORM models are not serializable by default
