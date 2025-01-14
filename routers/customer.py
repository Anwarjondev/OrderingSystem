from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import OrderCreate, ProductOrder
from utils import get_current_user, get_db
from models import Product, Order, OrderDetail

customer_router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)

@customer_router.post("/orders")
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    for product_order in order.products:
        product = db.query(Product).filter(Product.id == product_order.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_order.product_id} not found")
        if product.quantity < product_order.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient quantity for product {product.name}. Available: {product.quantity}, Requested: {product_order.quantity}"
            )
    
    new_order = Order(customer_id=current_user.id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    for product_order in order.products:
        product = db.query(Product).filter(Product.id == product_order.product_id).first()
        order_detail = OrderDetail(
            order_id=new_order.id,
            product_id=product_order.product_id,
            quantity=product_order.quantity
        )
        product.quantity -= product_order.quantity
        db.add(order_detail)
    db.commit()

    return {"detail": "Order created successfully", "order_id": new_order.id}

@customer_router.get("/products")
async def list_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    products = db.query(Product).all()
    return products

@customer_router.get("/orders")
async def list_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.customer_id == current_user.id).all()
    return orders
