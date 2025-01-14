from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ProductCreate
from utils import get_current_admin_user, get_db
from models import Order, Product

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@admin_router.post("/products", response_model=ProductCreate)
async def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_admin_user)
):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    # Explicitly convert SQLAlchemy object to Pydantic response model
    return ProductCreate.from_orm(new_product)

@admin_router.get("/products/{id}", response_model=ProductCreate)
async def read_product(
        id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_admin_user)
):
    product = db.query(Product).filter(Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductCreate.from_orm(product)



@admin_router.put("/products/{id}", response_model=ProductCreate)
async def update_product(
        id: int,
        product: ProductCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_admin_user)
):
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    # Explicitly use Pydantic model
    return ProductCreate.from_orm(db_product)

@admin_router.delete("/products/{id}")
async def delete_product(
        id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_admin_user)
):
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}

@admin_router.get("/orders")
async def read_orders(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_admin_user)
):
    orders = db.query(Order).all()
    return orders

@admin_router.get("/orders/{id}")
async def read_order(
        id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_admin_user)
):
    order = db.query(Order).filter(Order.id == id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order