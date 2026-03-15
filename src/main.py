import os
from fastapi import FastAPI
from mangum import Mangum

from src.routers import books

# ローカル実行時は root_path 不要
root_path = "" if os.environ.get("DYNAMODB_ENDPOINT") else "/prod"

app = FastAPI(
    title="Book Management API",
    version="1.0.0",
    root_path=root_path,
)

app.include_router(books.router)


@app.get("/health")
def health():
    return {"status": "ok"}


# Lambda handler
handler = Mangum(app, lifespan="off")
