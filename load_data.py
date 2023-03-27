from aws import get_aws_credentials_and_config

from botocore.exceptions import ClientError
import boto3

import json
import os

# Program

def load_data_to_dynamodb_table(table_name, data, aws_access_key_id, aws_secret_access_key, aws_session_token, region_name):
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
    )
    table = dynamodb.Table(table_name)
    
    for item in data:
        try:
            response = table.put_item(Item=item)
            print("Successfully inserted item:", item)
        except ClientError as e:
            print(f"Failed to insert item: {item}. Error: {e.response['Error']['Message']}")
            continue

def main():
    access_key_id, secret_access_key, region_name = get_aws_credentials_and_config('default')
    session_token = os.environ.get('AWS_SESSION_TOKEN')
    # Load data from the JSON file
    with open("a1.json", "r") as file:
        data = json.load(file)

    data = data['songs']

    # Specify the DynamoDB table name
    table_name = "music"

    # Load the data into the DynamoDB table
    load_data_to_dynamodb_table(table_name, data, access_key_id, secret_access_key, session_token, region_name)

if __name__ == "__main__":
    main()
