from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class UserRole(str, Enum):
    alumni = "alumni"
    admin = "admin"

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None

class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    student_id: str = Field(regex="^s3\d{6}$")

class UserIn(User):
    password: str

class UserInDB(User):
    role: UserRole
    hashed_password: str
    class Config:
        use_enum_values=True

class LoginCredentials(BaseModel):
    username: EmailStr
    password: str

class Certificate(BaseModel):
    certificate_number: int
    user_email: User

class Document(BaseModel):
    document_no: str
    type: str
    user_email: EmailStr