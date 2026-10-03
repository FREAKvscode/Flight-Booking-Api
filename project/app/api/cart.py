from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.cart import Cart
from app.models.product import Product
from app.models.user import User

router = APIRouter()


@router.post("/cart/{product_id}", status_code=201)
def add_to_cart(product_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail={"message": "Not found"})

    item = Cart(user_id=user.id, product_id=product_id)
    db.add(item)
    db.commit()
    return {"message": "Product add to card"}


@router.get("/cart")
def get_cart(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(Cart).filter(Cart.user_id == user.id).all()
    result = []
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            result.append({
                "id": item.id,
                "product_id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
            })
    return result


@router.delete("/cart/{item_id}")
def delete_from_cart(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Cart).filter(Cart.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail={"message": "Not found"})
    if item.user_id != user.id:
        raise HTTPException(status_code=403, detail={"message": "Forbidden for you"})

    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}

