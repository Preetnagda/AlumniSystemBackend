from abc import ABC, abstractmethod
from app.models import UserIn, UserInDB
class Db(ABC):    

    @abstractmethod
    def register_user(self, user: UserIn):
        pass

    @abstractmethod
    def get_user_from_email(self) -> UserInDB:
        pass
