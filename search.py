import requests
import json

def search_music(title, year_value, artist):
    print('CALLING SearchMusic API')
    url = 'https://1a19mamxg3.execute-api.us-east-1.amazonaws.com/default/SearchMusic'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': ''
    }
    body = {
        "body": {
            "title": title,
            "year": year_value,
            "artist": artist
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    print("SearchMusic Response")
    response_json = response.json()
    print(response_json)
    if response_json['statusCode'] == 200:
        # Return Array of subscriptions
        return response_json['body']
    else:
        return None

