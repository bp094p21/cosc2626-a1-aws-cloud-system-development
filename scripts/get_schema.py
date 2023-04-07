import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_subscriptions = dynamodb.Table('subscriptions')

# print the primary key schema of the table
key_schema = table_subscriptions.key_schema
print(key_schema)
