import requests
import json

def get_subscriptions(email):
    print('CALLING GetSubscriptions API')
    url = 'https://1a19mamxg3.execute-api.us-east-1.amazonaws.com/default/GetSubscriptions'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': ''
    }
    body = {
        "body": {
            "email": email,
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    print("Subscriptions Response")
    response_json = response.json()
    print(response_json)
    if response_json['statusCode'] == 200:
        # Return Array of subscriptions
        return response_json['body']
    else:
        return None


def subscribe_new(email, title, artist, year):
    print('CALLING SubscribeNew API')
    url = 'https://1a19mamxg3.execute-api.us-east-1.amazonaws.com/default/SubscribeNew'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': ''
    }
    body = {
        "body": {
            "email": email,
            "title": title,
            "artist": artist,
            "year": year,
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    print("SubscribeNew Response")
    response_json = response.json()
    print(response_json)
    if response_json['statusCode'] == 200:
        return True
    else:
        return None


def unsubscribe_music(email, subscription_id):
    print('CALLING UnsubscribeMusic API')
    url = 'https://1a19mamxg3.execute-api.us-east-1.amazonaws.com/default/UnsubscribeMusic'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': ''
    }
    body = {
        "body": {
            "email": email,
            "subscription_id": subscription_id
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    print("UnsubscribeMusic Response")
    response_json = response.json()
    print(response_json)
    if response_json['statusCode'] == 200:
        return True
    else:
        return None

