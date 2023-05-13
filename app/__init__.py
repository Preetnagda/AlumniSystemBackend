from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from .utils.config import Config
from .db import db

load_dotenv()

config = Config()
app = FastAPI()