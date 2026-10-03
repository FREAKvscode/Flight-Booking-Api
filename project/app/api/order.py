from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.cart import Cart
from app.models.order import Order
from app.models.product import Product
from app.models.user import User

router = APIRouter()


@router.post("/order", status_code=201)
def create_order(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not items:
        raise HTTPException(status_code=422, detail={"error": {"code": 422, "message": "Cart is empty"}})

    order_id = None
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            order = Order(user_id=user.id, product_id=product.id, price=product.price)
            db.add(order)
            db.flush()
            if order_id is None:
                order_id = order.id
        db.delete(item)

    db.commit()
    return {"order_id": order_id, "message": "Order is processed"}


@router.get("/order")
def list_orders(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    grouped: dict[int, dict] = {}
    for order in orders:
        if order.id not in grouped:
            grouped[order.id] = {"id": order.id, "products": [], "order_price": 0}
        grouped[order.id]["products"].append(order.product_id)
        grouped[order.id]["order_price"] += order.price
    return list(grouped.values())

