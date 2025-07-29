import pytest
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from app.database import Base, engine


def test_database_connection():
    connection = engine.connect()
    assert connection is not None
    connection.close()


def test_database_setup():
    Base.metadata.create_all(bind=engine)
    inspector = sqlalchemy.inspect(engine)
    assert 'products' in inspector.get_table_names()
    assert 'comments' in inspector.get_table_names() 
