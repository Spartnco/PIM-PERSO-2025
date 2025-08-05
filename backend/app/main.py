from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="PIM API")


class Product(BaseModel):
    id: int
    sku: str
    name: str


# Temporary in-memory store
_products = [
    Product(id=1, sku="SKU001", name="Example product"),
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products", response_model=list[Product])
def list_products() -> list[Product]:
    return _products
