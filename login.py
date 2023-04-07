import requests
import json

def login_user(email, password):
    print('CALLING LoginUser API')
    url = 'https://1a19mamxg3.execute-api.us-east-1.amazonaws.com/default/LoginUser'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': ''
    }
    body = {
        "body": {
            "email": email,
            "password": password
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    print("Login Response")
    response_json = response.json()
    print(response_json)
    if response_json['statusCode'] == 200:
        return json.loads(response_json['body'])
    else:
        return None

