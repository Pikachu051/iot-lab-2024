from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
import uuid

from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)
    detail = Column(String, index=True)
    short_desc = Column(String, index=True)
    categories = Column(ARRAY(String), index=True)

class Student(Base):
    __tablename__ = 'students'

    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)
    dob = Column(String, index=True)
    gender = Column(String, index=True)

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    img = Column(String, index=True)
    price = Column(Integer, index=True)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    quantity = Column(Integer, index=True)
    total_price = Column(Integer, index=True)
    is_completed = Column(Boolean, index=True)
    order_time = Column(String, index=True)
    note = Column(String, index=True)