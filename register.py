import requests
import json

def register_user(email, username, password, api=False):
    if api:
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
        pass

    else:
        # If email matches w/ table, show "Email already exists" on register page
        response = table_login.query(
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        if response['Items']:
            # Display an error message if the email already exists
            error = 'Email already exists.'
            return None
        # If email is unique, put new user info in table
        table_login.put_item(
            Item={
                'email': email,
                'username': username,
                'password': password
            }
        )
        return True

