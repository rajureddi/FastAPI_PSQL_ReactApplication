from  fastapi import FastAPI,Depends
from model import product
from database import SessionLocal,engine
app = FastAPI()
import database_model
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_model.Base.metadata.create_all(bind=engine)
products = [
    product(id=1,name="shoes",desc="nike shoes",price=500),
    product(id=2,name="shoes",desc="bata shoes",price=600),
   
           ]
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

def init_db():
    db=SessionLocal()
    count = db.query(database_model.product).count
    if count ==0:
        for product in products:
            db.add(database_model.product(**product.model_dump()))
        db.commit()
    
init_db()
    
    
@app.get("/")
def greet():
    return "welcome to fastapi learning"

@app.get("/all products")
def all_products(db:Session =Depends(get_db) ):
    #db =SessionLocal()
    #db.query()
    db_products = db.query(database_model.product).all()
    
    return db_products


@app.get("/products/{id}")
def fetech_product_by_id(id:int,db:Session =Depends(get_db) ):
    #for prod in products:
        #if prod.id == id:
            #return prod  
    #return "Product not found"
    db_product = db.query(database_model.product).filter(database_model.product.id==id).first()
    if db_product:
        return db_product
    return "product not found"

@app.post("/products")
def add_products(product: product, db: Session = Depends(get_db)):

    existing = db.query(database_model.product)\
                 .filter(database_model.product.id == product.id)\
                 .first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Product with this ID already exists"
        )

    db_product = database_model.product(**product.model_dump())
    db.add(db_product)
    db.commit()
    return db_product

@app.put("/products")
def update_items(id:int,product:product,db:Session =Depends(get_db)):
    # for i in range(len(products)):
    #     if products[i].id ==id:
    #         products[i] = product
    #         return "product added successfully"
    # return "No prodcut found"
    db_product = db.query(database_model.product).filter(database_model.product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.price=product.price
        db_product.desc = product.desc
        db.commit()
        return "Product updated"
    else:
        return "no product found"
        
        
        
@app.delete("/products")
def delete_products(id:int,db:Session =Depends(get_db)):
    db_product = db.query(database_model.product).filter(database_model.product.id==id).first()

    # for i in range(len(products)):
    #     if products[i].id ==id:
    #         del products[i]
    #         return "product removed successfully"
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product removed successfully"
    else:
        return "Product not found"
              
  