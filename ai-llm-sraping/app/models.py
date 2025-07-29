from sqlalchemy import Column, Integer, String, Text

from .database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    image_urls = Column(Text)
    comments = Column(Text)
    sentiments = Column(Text) 

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    text = Column(Text)
    sentiment = Column(String) 