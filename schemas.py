from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class ProductCreate(BaseModel):
    name: str
    quantity: int
    price: int
    
    class Config:
        orm_mode = True

class ProductOrder(BaseModel): 
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_id: int
    products: list[ProductOrder]

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    products: list[ProductOrder]

    class Config:
        orm_mode = True