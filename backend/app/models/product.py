from sqlalchemy import Column, Integer, String
from app.database.connection import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    sku = Column(String, unique=True, nullable=False)

    name = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)

    aisle = Column(String, nullable=False)

    shelf = Column(String, nullable=False)