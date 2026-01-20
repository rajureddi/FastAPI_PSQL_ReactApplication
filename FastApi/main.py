from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import database_model
from model import product

app = FastAPI()

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ DB INIT ------------------
database_model.Base.metadata.create_all(bind=engine)

# ------------------ DB DEPENDENCY ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ ROOT ------------------
@app.get("/")
def greet():
    return {"message": "Welcome to FastAPI learning"}

# ------------------ GET ALL ------------------
@app.get("/all products")
def all_products(db: Session = Depends(get_db)):
    return db.query(database_model.product).all()

# ------------------ GET BY ID ------------------
@app.get("/products/{id}")
def fetch_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_model.product)
        .filter(database_model.product.id == id)
        .first()
    )

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return db_product

# ------------------ ADD PRODUCT ------------------
@app.post("/products", status_code=201)
def add_products(product: product, db: Session = Depends(get_db)):

    existing = (
        db.query(database_model.product)
        .filter(database_model.product.id == product.id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Product with this ID already exists"
        )

    db_product = database_model.product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

# ------------------ UPDATE PRODUCT ------------------
@app.put("/products")
def update_items(id: int, product: product, db: Session = Depends(get_db)):

    db_product = (
        db.query(database_model.product)
        .filter(database_model.product.id == id)
        .first()
    )

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.desc = product.desc
    db_product.price = product.price

    db.commit()
    db.refresh(db_product)

    return db_product

# ------------------ DELETE PRODUCT ------------------
@app.delete("/products")
def delete_products(id: int, db: Session = Depends(get_db)):

    db_product = (
        db.query(database_model.product)
        .filter(database_model.product.id == id)
        .first()
    )

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()

    return {"message": "Product removed successfully"}
