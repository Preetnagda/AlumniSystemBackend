from app.models import AlumniInDB, Alumni
from .abstract import Db as AbstractDb

class Db(AbstractDb):
    
    def __init__(self):
        self.users_db = {
            "s3323211": {
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string",
                "student_id": "s3323211",
                "hashed_password": "$2b$12$6QQ3L9qd7CFIERDX6Ac7oeGCE2BTTdMA4IbmV5BMUTnxCDCp.F3By"
            }
        }

    def register_alumni(self, alumni: AlumniInDB) -> Alumni:
        if alumni.student_id in self.users_db:
            return False
        self.users_db[alumni.student_id] = alumni.dict()
        print(self.users_db)
        return Alumni.parse_obj(alumni)
    
    def get_alumni_from_studentid(self, student_id) -> AlumniInDB:
        print(student_id)
        if student_id not in self.users_db:
            return None
        alumni = self.users_db[student_id]
        return AlumniInDB.parse_obj(alumni)

    def get_alumni_from_email(self, email) -> AlumniInDB:
        if email not in self.users_db:
            return None
        alumni = self.users_db[email]
        return AlumniInDB.parse_obj(alumni)