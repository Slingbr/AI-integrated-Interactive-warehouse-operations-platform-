from fastapi import FastAPI
from app.routes.product_routes import router as product_router
from app.models import product, warehouse_location
from app.routes.worker_routes import router as worker_router
from app.routes.order_routes import router as order_router
from app.models.order import Order
from app.models.order_item import OrderItem
app = FastAPI()

app.include_router(product_router)
app.include_router(worker_router)
app.include_router(order_router)

@app.get("/")
def root():
    return {"message": "AI Warehouse System API Running"}