from fastapi import FastAPI
from app.routes.product_routes import router as product_router
from app.models import product, warehouse_location
app = FastAPI()

app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "AI Warehouse System API Running"}