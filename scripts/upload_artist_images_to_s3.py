from aws import get_aws_credentials_and_config
import json
import os
import boto3
import requests
import io

# Load the JSON file
access_key_id, secret_access_key, region_name = get_aws_credentials_and_config('default')
session_token = os.environ.get('AWS_SESSION_TOKEN')
with open('a1.json') as f:
    data = json.load(f)

data = data['songs']

# Create an S3 client
# s3 = boto3.client('s3')

s3 = boto3.client("s3")

# Loop through the data and download/upload each image
for item in data:
    image_url = item['img_url']
    filename = os.path.basename(image_url)
    response = requests.get(image_url)
    if response.status_code == 200:
        # Create a BytesIO object from the response content
        file = io.BytesIO(response.content)
        # Upload the file to S3
        s3.upload_fileobj(file, 's3491222-test', filename)
        print(f'{filename} uploaded to S3')
    else:
        print(f'Error downloading {image_url}: {response.status_code}')
