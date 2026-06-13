from fastapi import FastAPI
from app.routes.product_routes import router as product_router

app = FastAPI()

app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "AI Warehouse System API Running"}