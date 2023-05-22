from app import app
from app.routers.auth import router as auth_router
from app.routers.alumni import router as alumni_router
from app.routers.external import router as external_router

app.include_router(auth_router)
app.include_router(alumni_router)
app.include_router(external_router)

@app.get("/")
def health_check():
    return {"health": "OK"}