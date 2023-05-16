from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from app.models import UserIn, UserInDB, Token, UserRole
from app import db, config
from app.utils.auth import encode_password, authenticate_credentials, \
    create_access_token, AuthCredentialDependency, get_current_user
from datetime import timedelta
from app.utils.exceptions import CredentialException, TokenException

router = APIRouter(
    tags=["auth"],
)

@router.post("/login", response_model=Token)
def login(login_credentials: Annotated[AuthCredentialDependency, Depends()]):
    user = authenticate_credentials(login_credentials)
    if not user:
        raise CredentialException
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(user: UserIn):
   user_dict = user.dict()
   user_dict["hashed_password"] = encode_password(user.password)
   user_dict["role"] = UserRole.alumni
   user_in_db = UserInDB.parse_obj(user_dict)
   return db.register_user(user_in_db)

@router.post("/register-admin")
def register_admin(user: UserIn, current_user: Annotated[UserInDB, Depends(get_current_user)]):
   if current_user.role != UserRole.admin:
       raise TokenException
   user_dict = user.dict()
   user_dict["hashed_password"] = encode_password(user.password)
   user_dict["role"] = UserRole.admin
   user_in_db = UserInDB.parse_obj(user_dict)
   return db.register_user(user_in_db)