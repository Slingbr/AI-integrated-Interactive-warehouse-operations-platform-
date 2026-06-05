from app.database.connection import Base, engine
from app.models.product import Product

Base.metadata.create_all(bind=engine)

print("Database table creation test successfull.")
print("Products created")