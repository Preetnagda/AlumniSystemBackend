from pydantic import BaseModel, EmailStr, Field
from fastapi import Form

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None

class Alumni(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    student_id: str = Field(regex="^s3\d{6}$")

class AlumniIn(Alumni):
    password: str

class AlumniInDB(Alumni):
    hashed_password: str

class LoginCredentials(BaseModel):
    username: EmailStr | str = Field(regex="^s3\d{6}$")
    password: str

class Certificate(BaseModel):
    certificate_number: int
    alumni_email: Alumni