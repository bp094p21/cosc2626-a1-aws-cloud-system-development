import boto3

def create_table():
    # create a client object for DynamoDB
    dynamodb = boto3.client('dynamodb')

    # create a new DynamoDB table
    table_name = 'subscriptions'
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
        {
            'AttributeName': 'subscription_id',
            'KeyType': 'HASH'
        },
        {
            "AttributeName": "email",
            "KeyType": "RANGE"
        },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'subscription_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
    )

    # wait for the table to be created before continuing
    dynamodb.get_waiter('table_exists').wait(TableName=table_name)

    # print the table description to confirm creation
    print(dynamodb.describe_table(TableName=table_name))

def main():
    # access_key_id, secret_access_key, region_name = get_aws_credentials_and_config('default')
    # session_token = os.environ.get('AWS_SESSION_TOKEN')
    # print(f"AWS Access Key ID: {access_key_id}")
    # print(f"AWS Secret Access Key: {secret_access_key}")
    # print(f"AWS Session Token: {session_token}")
    # print(f"AWS Region Name: {region_name}")
    create_table()

if __name__ == '__main__':
    main()

