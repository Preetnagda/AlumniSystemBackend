from app.models import AlumniInDB, Alumni
from .abstract import Db as AbstractDb
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class Db(AbstractDb):

    ALUMNI_TABLE_NAME = 'alumni'
    CERTIFICATE_TABLE_NAME = 'certificate'

    def __init__(self):
        self.engine = boto3.resource('dynamodb')
        self.alumni_table = self.engine.Table(self.ALUMNI_TABLE_NAME)
        self.certificate_table = self.engine.Table(self.CERTIFICATE_TABLE_NAME)

    def register_alumni(self, alumni: AlumniInDB) -> Alumni:
        if self.get_alumni_from_email(alumni.email) is not None:
            return False
        try:
            self.alumni_table.put_item(
                Item=alumni.dict()
            )
        except ClientError as err:
            print(err)
            return False
        
        return Alumni.parse_obj(alumni)

    def get_alumni_from_email(self, email) -> AlumniInDB:
        get_item_response = self.alumni_table.get_item(Key={'email':email})
        if "Item" not in get_item_response:
            return None
        alumni = get_item_response["Item"]
        return AlumniInDB.parse_obj(alumni)