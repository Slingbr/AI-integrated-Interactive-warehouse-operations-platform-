from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(db: Session, product: ProductCreate) -> Product:
    new_product = Product(
        sku=product.sku,
        name=product.name,
        quantity=product.quantity,
        aisle=product.aisle,
        shelf=product.shelf,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product



def update_product(
    db: Session,
    product_id: int,
    product: ProductCreate
) -> Product:

    existing_product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    for key, value in product.model_dump().items():
        setattr(existing_product, key, value)

    db.commit()
    db.refresh(existing_product)

    return existing_product