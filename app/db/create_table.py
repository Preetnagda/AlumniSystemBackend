import boto3
from botocore.exceptions import ClientError

def create_alumni_table():
    try:
        engine = boto3.resource('dynamodb')
        alumni_table = engine.create_table(
            TableName="alumni",
            KeySchema=[
                {'AttributeName': 'email', 'KeyType': 'HASH'},  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'email', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1})
        alumni_table.wait_until_exists()
    except ClientError as err:
        print(
            "Couldn't create table. %s: %s",
            err.response['Error']['Code'], err.response['Error']['Message'])
        raise
    else:
        return alumni_table

def create_certificate_table():
    try:
        engine = boto3.resource('dynamodb')
        alumni_table = engine.create_table(
            TableName="certificate",
            KeySchema=[
                {'AttributeName': 'certificate_no', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'alumni_email', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'alumni_email', 'AttributeType': 'S'},
                {'AttributeName': 'certificate_no', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1})
        alumni_table.wait_until_exists()
    except ClientError as err:
        print(
            "Couldn't create table. %s: %s",
            err.response['Error']['Code'], err.response['Error']['Message'])
        raise
    else:
        return alumni_table
    
if __name__ == '__main__':
    create_certificate_table()
    create_alumni_table()