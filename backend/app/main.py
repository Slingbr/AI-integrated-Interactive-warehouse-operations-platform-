from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "AI Warehouse System API Running"}