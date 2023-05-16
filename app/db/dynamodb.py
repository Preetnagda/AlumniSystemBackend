from app.models import UserInDB, User
from .abstract import Db as AbstractDb
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class Db(AbstractDb):

    USER_TABLE_NAME = 'user'
    DOCUMENT_TABLE_NAME = 'document'

    def __init__(self):
        self.engine = boto3.resource('dynamodb')
        self.user_table = self.engine.Table(self.USER_TABLE_NAME)
        self.certificate_table = self.engine.Table(self.DOCUMENT_TABLE_NAME)

    def register_user(self, user: UserInDB) -> User:
        if self.get_user_from_email(user.email) is not None:
            return False
        try:
            self.user_table.put_item(
                Item=user.dict()
            )
        except ClientError as err:
            print(err)
            return False
        
        return user.parse_obj(user)

    def get_user_from_email(self, email) -> UserInDB:
        get_item_response = self.user_table.get_item(Key={'email':email})
        if "Item" not in get_item_response:
            return None
        user = get_item_response["Item"]
        return UserInDB.parse_obj(user)