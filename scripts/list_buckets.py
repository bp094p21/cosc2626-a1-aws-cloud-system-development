import boto3

# Retrieve the list of existing buckets
# s3 = boto3.client('s3')
s3 = boto3.client("s3")
response = s3.list_buckets()
print('s3.list_buckets():')
print(response['Buckets'])
print('type(s3.list_buckets()):')
print(type(response['Buckets']))

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')