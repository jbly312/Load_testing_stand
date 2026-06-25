from pydantic import BaseModel

class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock: int
    description: str
    rating: float

    class Config:
        from_attributes = True

class OrderIn(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int


    class Config:
        from_attributes = True
