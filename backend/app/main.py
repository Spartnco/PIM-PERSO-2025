from fastapi import FastAPI, HTTPException
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Field, Session, create_engine, select


sqlite_url = "sqlite://"
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

app = FastAPI(title="PIM API")


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sku: str
    name: str


class ProductCreate(SQLModel):
    sku: str
    name: str


SQLModel.metadata.create_all(engine)
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/products", response_model=Product)
def create_product(product: ProductCreate) -> Product:
    with Session(engine) as session:
        db_product = Product.model_validate(product)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product


@app.get("/products", response_model=list[Product])
def list_products() -> list[Product]:
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int) -> Product:
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int) -> dict[str, bool]:
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        session.delete(product)
        session.commit()
        return {"ok": True}
