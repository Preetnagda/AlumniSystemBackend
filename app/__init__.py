from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from .utils.config import Config
from .db import db
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

config = Config()
app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)