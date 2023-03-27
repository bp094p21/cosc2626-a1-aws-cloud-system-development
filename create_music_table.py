import boto3
import configparser
import os

def get_aws_credentials_and_config(profile_name='default'):

    # Get credentials from ~/.aws/credentials
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.expanduser('~'), '.aws', 'credentials')
    
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Credentials file not found at {config_file_path}")

    config.read(config_file_path)
    
    if profile_name not in config.sections():
        raise ValueError(f"Profile '{profile_name}' not found in credentials file")

    access_key_id = config.get(profile_name, 'aws_access_key_id')
    secret_access_key = config.get(profile_name, 'aws_secret_access_key')

    # Get config from ~/.aws/config
    config_config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.expanduser('~'), '.aws', 'config')
    
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Config file not found at {config_file_path}")

    config_config.read(config_file_path)
    
    config_profile_name = f"profile {profile_name}" if profile_name != 'default' else 'default'
    if config_profile_name not in config_config.sections():
        raise ValueError(f"Profile '{profile_name}' not found in config file")

    region_name = config_config.get(config_profile_name, 'region')

    # Return credentials and config

    return access_key_id, secret_access_key, region_name

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

if __name__ == '__main__':
    access_key_id, secret_access_key, region_name = get_aws_credentials_and_config('default')
    session_token = os.environ.get('AWS_SESSION_TOKEN')
    print(f"AWS Access Key ID: {access_key_id}")
    print(f"AWS Secret Access Key: {secret_access_key}")
    create_table(access_key_id, secret_access_key, region_name, session_token)

