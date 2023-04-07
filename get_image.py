import requests
import json

def get_image(artist_name):
    print('CALLING API')
    url = 'https://u78rbsvgx0.execute-api.us-east-1.amazonaws.com/default/GetImage'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'R54sah6pV95LdQf42pYVB56EkAoB0K67agtjg5Ta'
    }
    body = {
        "body": {
            "artist_name": artist_name
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    response_json = response.json()
    if response_json['statusCode'] == 200:
        return response_json['body']['artist_image_url']
    else:
        return None

