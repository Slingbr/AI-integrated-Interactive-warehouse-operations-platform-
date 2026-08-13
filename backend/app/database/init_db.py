from app.database.connection import Base, engine
from app.models.product import Product
from app.models.warehouse_location import WarehouseLocation

Base.metadata.create_all(bind=engine)

print("Database table creation test successfull.")
print("Products created")