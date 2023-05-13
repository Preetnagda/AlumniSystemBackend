from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from app.models import AlumniIn, AlumniInDB, Token
from app import db, config
from app.utils.auth import encode_password, authenticate_credentials, \
    create_access_token, AuthCredentialDependency
from datetime import timedelta

router = APIRouter(
    tags=["auth"],
)

@router.post("/login", response_model=Token)
def login(login_credentials: Annotated[AuthCredentialDependency, Depends()]):
    alumni = authenticate_credentials(login_credentials)
    if not alumni:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"student_id": alumni.student_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(alumni: AlumniIn):
   alumni_dict = alumni.dict()
   alumni_dict["hashed_password"] = encode_password(alumni.password)
   alumni_in_db = AlumniInDB.parse_obj(alumni_dict)
   return db.register_alumni(alumni_in_db)