import pytest
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import Comment, Product


def test_product_model():
    session: Session = SessionLocal()
    new_product = Product(title="Test Product", image_urls="http://example.com/image.jpg", comments="Great product!", sentiments="Great product!: positive")
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    assert new_product.id is not None
    assert new_product.title == "Test Product"
    session.close()


def test_comment_model():
    session: Session = SessionLocal()
    new_comment = Comment(product_id=1, text="Great product!", sentiment="positive")
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)

    assert new_comment.id is not None
    assert new_comment.text == "Great product!"
    session.close() 