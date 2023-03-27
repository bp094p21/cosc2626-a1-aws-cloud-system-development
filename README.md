# Database Scripts

This repo contains scripts to manage database requirements using DynamoDB via the AWS CLI.

We are using Python3 here.

## Getting Started

- ensure Python3 is installed
- create a Python3 virtual env
- Install dependencies using `requirements.txt`
- Configure AWS credentials & config (e.g. `aws configure`)
- Set `AWS_SESSION_TOKEN` environment variable (e.g. `export AWS_SESSION_TOKEN=xyz`)

Run script:
```bash
python3 create_music_table.py
```

## create_music_table
- reads AWS credentials and config in `~/.aws/*`.
- reads `AWS_SESSION_TOKEN` env var

## Creating Python Virtual Env

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
