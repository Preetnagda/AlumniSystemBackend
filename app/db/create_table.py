import boto3
from botocore.exceptions import ClientError

def create_user_table():
    try:
        engine = boto3.resource('dynamodb')
        user_table = engine.create_table(
            TableName="user",
            KeySchema=[
                {'AttributeName': 'email', 'KeyType': 'HASH'},  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'email', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1})
        user_table.wait_until_exists()
    except ClientError as err:
        print(
            "Couldn't create table. %s: %s",
            err.response['Error']['Code'], err.response['Error']['Message'])
        raise
    else:
        return user_table

def create_document_table():
    try:
        engine = boto3.resource('dynamodb')
        document_table = engine.create_table(
            TableName="document",
            KeySchema=[
                {'AttributeName': 'document_no', 'KeyType': 'HASH'},  # Partition key
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user_emal-index',
                    'KeySchema': [{
                        'AttributeName': 'user_email', 
                        'KeyType': 'HASH'
                    }],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
                }
            ],
            AttributeDefinitions=[
                {'AttributeName': 'document_no', 'AttributeType': 'S'},
                {'AttributeName': 'user_email', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1})
        document_table.wait_until_exists()
    except ClientError as err:
        print(
            "Couldn't create table. %s: %s",
            err.response['Error']['Code'], err.response['Error']['Message'])
        raise
    else:
        return document_table
    
if __name__ == '__main__':
    create_document_table()
    # create_user_table()