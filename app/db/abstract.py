from abc import ABC, abstractmethod
from app.models import AlumniIn, AlumniInDB
class Db(ABC):    

    @abstractmethod
    def register_alumni(self, alumni: AlumniIn):
        pass

    @abstractmethod
    def get_alumni_from_email(self) -> AlumniInDB:
        pass

    @abstractmethod
    def get_alumni_from_studentid(self) -> AlumniInDB:
        pass
        
