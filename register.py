import requests
import json

def register_user(email, username, password):
    print('CALLING RegisterUser API')
    url = 'https://1a19mamxg3.execute-api.us-east-1.amazonaws.com/default/RegisterUser'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': ''
    }
    body = {
        "body": {
            "email": email,
            "username": username,
            "password": password
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    print('Response')
    print(response)
    response_json = response.json()
    print('Response.json()')
    print(response_json)
    if response_json['statusCode'] == 200:
        return True
    else:
        return None

