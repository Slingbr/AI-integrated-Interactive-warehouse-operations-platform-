from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(db: Session, product: ProductCreate) -> Product:
    new_product = Product(
        sku=product.sku,
        name=product.name,
        quantity=product.quantity,
        aisle=product.aise,
        shelf=product.shelf,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product