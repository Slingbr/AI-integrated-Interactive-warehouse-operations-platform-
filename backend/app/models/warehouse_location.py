from sqlalchemy import Column, Integer, String

from app.database.connection import Base


class WarehouseLocation(Base):
    __tablename__ = "warehouse_locations"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String, unique=True, nullable=False)

    name = Column(String, nullable=False)

    location_type = Column(String, nullable=False)

    x_coordinate = Column(Integer, nullable=False)

    y_coordinate = Column(Integer, nullable=False)