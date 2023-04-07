# Database Scripts

This repo contains scripts to manage database requirements using DynamoDB via the AWS CLI.

We are using Python3 here.

## Getting Started

- ensure Python3 is installed
- create a Python3 virtual env
- Install dependencies using `requirements.txt`
  - `pip3 install -r requirements.txt`
- Configure AWS credentials & config (e.g. `aws configure`)
  - Might need to manually add `aws_session_token` to `~/.aws/credentials`
  - Or, also set `AWS_SESSION_TOKEN` environment variable (e.g. `export AWS_SESSION_TOKEN=xyz`)

## Tasks

### Task 1.2 - Music Table

Run the following script:
```bash
python3 create_music_table.py
```

### Task 1.3 - Load Data

Run the following script:
```bash
python3 load_music_data_from_json.py
```

### Task 2 - Upload Artist Images to S3

Run the following script:
```bash
python3 upload_artist_images_to_s3.py
```

### Task 3,4,5
- Use `main` branch
- Flask app contained in `app.py`
- This program uses imported functions to talk to AWS Cloud
  - imported functions should be given argument `api=False` to fetch data without using API Gateway. Example:
    - This fetches using boto3 from EC2: `user = login_user(email, password, dynamodb, api=False)`
    - This fetches using Lambda functions via API Gateway: `user = login_user(email, password, dynamodb, api=True)`

### Task 6
- Use `lambda-only` branch or `main` branch and set `api=True` for all imported functions in `app.py`

## aws.py
- reads AWS credentials and config in `~/.aws/*`.
- reads `AWS_SESSION_TOKEN` env var

## Notes

### create_music_table.py
- DynamoDB is schema-less for non-key attributes, so you can add additional attributes (e.g. `year`, `web_url`, `image_url`) when you're inserting items into the table without specifying them in the table schema.

### Creating Virtual Environment & Installing Dependencies

```bash
pip3 install venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
