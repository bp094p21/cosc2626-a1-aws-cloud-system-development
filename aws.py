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