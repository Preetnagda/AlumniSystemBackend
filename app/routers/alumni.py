from fastapi import APIRouter
from typing import Annotated
from app.models import UserInDB, User
from app.utils.auth import get_current_user
from fastapi import Depends
from app import db

router = APIRouter(tags=["Alumni"])

@router.get("/get_documents")
def get_documents(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    return db.get_user_documents(current_user)

@router.get("/get_current_user")
def get_documents(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    return User.parse_obj(current_user.dict())