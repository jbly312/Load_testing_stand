from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop API - нагрузочное тестирование")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products", response_model=list[schemas.ProductOut])
def list_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Product).offset(skip).limit(limit).all()

@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/orders", response_model=schemas.OrderOut, status_code=201)
def create_order(order: schemas.OrderIn, db: Session = Depends(get_db)):
    new_order = models.Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

