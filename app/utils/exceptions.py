from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class TokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Could not validate credentials", 
            headers = {"WWW-Authenticate": "Bearer"}
        )

class CredentialException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )