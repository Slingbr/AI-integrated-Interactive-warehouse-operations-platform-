from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base



class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)

    current_location_id = Column(
        Integer,
        ForeignKey("warehouse_locations.id"),
        nullable=True
    )

    current_location = relationship("WarehouseLocation")