from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from .database import Base


# Responsible for creating the table in the database
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
