from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from app import config, db
from app.models import LoginCredentials, AlumniInDB, TokenData
from pydantic import EmailStr
from datetime import timedelta, datetime
from fastapi.param_functions import Form, Body

auth_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthCredentialDependency(OAuth2PasswordRequestForm):

    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),

    ):
        super().__init__(
            grant_type="password",
            username=username,
            password=password,
            scope=""
        )

def is_email(value: str):
    try:
        EmailStr.validate(value)
        return True
    except:
        return False

def encode_password(password: str):
    return pwd_context.hash(password)

def verify_hashed_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_credentials(login_credentials: LoginCredentials) -> AlumniInDB:
    if is_email(login_credentials.username):
        alumni = db.get_alumni_from_email(login_credentials.username)
    else:
        alumni = db.get_alumni_from_studentid(login_credentials.username)
    if not alumni:
        return False
    is_password_verified = verify_hashed_password(login_credentials.password, alumni.hashed_password)
    if not is_password_verified:
        return False
    
    return alumni

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ENCRYPTION_ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(auth_scheme)]):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ENCRYPTION_ALGORITHM])
        print(payload)
        student_id: str = payload.get("student_id")
        if student_id is None:
            raise credentials_exception
        token_data = TokenData(student_id=student_id)
    except JWTError:
        raise credentials_exception
    alumni = db.get_alumni_from_studentid(token_data.student_id)
    if alumni is None:
        raise credentials_exception
    return alumni