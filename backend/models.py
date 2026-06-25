from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    category = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    description = Column(String)
    rating = Column(Float)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String,unique=True)
    address = Column(String)
    phone = Column(String)

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
