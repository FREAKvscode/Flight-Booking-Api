from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import ProfileUpdateSchema

router = APIRouter()


@router.get("/profile")
def get_profile(user: User = Depends(get_current_user)):
    return {"user": {"id": user.id, "fio": user.fio, "avatar": user.avatar, "email": user.email}}


@router.patch("/profile")
def update_profile(
    data: ProfileUpdateSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.fio is not None:
        user.fio = data.fio
    if data.avatar is not None:
        user.avatar = data.avatar
    db.commit()
    return {"message": "data updated successfully"}

