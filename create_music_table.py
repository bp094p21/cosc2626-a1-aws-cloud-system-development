import boto3
import os
from aws import get_aws_credentials_and_config

def create_table(aws_access_key_id, aws_secret_access_key, region_name, aws_session_token):

    # Create a DynamoDB resource using Boto3
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
    )

    # Define the "music" table schema
    params = {
        "TableName": "music",
        "KeySchema": [
            {"AttributeName": "title", "KeyType": "HASH"},
            {"AttributeName": "artist", "KeyType": "RANGE"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "title", "AttributeType": "S"},
            {"AttributeName": "artist", "AttributeType": "S"},
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5,
        },
    }

    # Create the "music" table
    table = dynamodb.create_table(**params)
    table.meta.client.get_waiter("table_exists").wait(TableName="music")
    print("Table created.")


def main():
    access_key_id, secret_access_key, region_name = get_aws_credentials_and_config('default')
    session_token = os.environ.get('AWS_SESSION_TOKEN')
    print(f"AWS Access Key ID: {access_key_id}")
    print(f"AWS Secret Access Key: {secret_access_key}")
    print(f"AWS Session Token: {session_token}")
    print(f"AWS Region Name: {region_name}")
    create_table(access_key_id, secret_access_key, region_name, session_token)


if __name__ == '__main__':
    main()

