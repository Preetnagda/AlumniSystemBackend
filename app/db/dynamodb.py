from app.models import UserInDB, User, Document
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
        self.document_table = self.engine.Table(self.DOCUMENT_TABLE_NAME)

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
    
    def add_document(self, document_no, user: User, type):
        try:
            self.document_table.put_item(
                Item={
                    "document_no": document_no,
                    "user_email": user.email,
                    "type": type
                }
            )
        except ClientError as err:
            print(err)
            return False            
        
    def get_user_documents(self, user:User):
        try:
            response = self.document_table.query(
                IndexName='user_email-index',
                KeyConditionExpression=Key('user_email').eq(user.email)
            )
            return response["Items"]
        except ClientError as err:
            print(err)
            return False
        
    def get_document(self, document_no: str) -> Document:
        try:
            response = self.document_table.get_item(
                Key={'document_no':document_no}
            )
            return Document.parse_obj(response["Item"])
        except ClientError as err:
            print(err)
            return False