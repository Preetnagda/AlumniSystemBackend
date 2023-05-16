from app import app
from typing import Annotated
from fastapi import Depends
from app.routers.auth import router as auth_router
from .utils.auth import get_current_user
from .models import UserInDB

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items/")
async def read_items(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    return {"current_user": current_user}