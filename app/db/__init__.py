from .dynamodb import Db
from .abstract import Db as AbstractDB

if not issubclass(Db, AbstractDB):
    raise Exception("Database layer not valid")

db = Db()