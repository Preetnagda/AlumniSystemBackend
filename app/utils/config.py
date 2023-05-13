import os

class Config():

    def __init__(self):

        try:
            self.SECRET_KEY = os.environ.get("SECRET_KEY")
            self.ENCRYPTION_ALGORITHM = os.environ.get("ENCRYPTION_ALGORITHM")
            self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        except:
            raise Exception("Environment variables not loaded")