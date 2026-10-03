from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import SignupSchema, LoginSchema

router = APIRouter()


@router.post("/signup", status_code=201)
def signup(data: SignupSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=422, detail={"message": "Validation error", "email": "already exists"})

    user = User(
        fio=data.fio,
        email=data.email,
        password=hash_password(data.password),
        role="client",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id, user.role)
    return {"user_token": token}


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail={"password": "Login failed"})

    token = create_token(user.id, user.role)
    return {"user_token": token}

