from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.services import product_service
router = APIRouter()


@router.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
     return product_service.create_product(db, product)

@router.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product




@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_service.delete_product(db, product_id)