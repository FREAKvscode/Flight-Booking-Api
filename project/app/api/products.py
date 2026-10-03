from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db.session import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreateSchema, ProductUpdateSchema

router = APIRouter()


@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [{"id": p.id, "name": p.name, "description": p.description, "price": p.price} for p in products]


@router.post("/product", status_code=201)
def create_product(
    data: ProductCreateSchema,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    product = Product(name=data.name, description=data.description, price=data.price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"id": product.id, "message": "Product added"}


@router.patch("/product/{product_id}")
def update_product(
    product_id: int,
    data: ProductUpdateSchema,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail={"message": "Not found"})

    if data.name is not None:
        product.name = data.name
    if data.description is not None:
        product.description = data.description
    if data.price is not None:
        product.price = data.price
    db.commit()
    db.refresh(product)
    return {"id": product.id, "name": product.name, "description": product.description, "price": product.price}


@router.delete("/product/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail={"message": "Not found"})
    db.delete(product)
    db.commit()
    return {"message": "Product removed"}


