from app.database.connection import SessionLocal
from app.models.product import Product

db = SessionLocal()

new_product = Product(
    sku="WM100",
    name="Wireless Mouse",
    quantity=250,
    aisle="A",
    shelf="12"
)

db.add(new_product)
db.commit()

print("Product inserted successfully.")

db.close()