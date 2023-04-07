from get_image import get_image
import requests
import json

def search_music(title, year_value, artist, dynamodb, api=False):
    if api:
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
    else:
        table_music = dynamodb.Table('music')
        conditions = []
        values = {}

        if title:
            print('YES TITLE')
            conditions.append('begins_with(title, :title)')
            values[':title'] = title
        if artist:
            print('YES ARTIST')
            conditions.append('begins_with(artist, :artist)')
            values[':artist'] = artist
        if year_value:
            print('YES YEAR')
            conditions.append('#yr = :year')
            values[':year'] = year_value
            expression_attribute_names = {'#yr': 'year'}

            condition_str = ' AND '.join(conditions)
            response = table_music.scan(
                FilterExpression=condition_str,
                ExpressionAttributeValues=values,
                ExpressionAttributeNames=expression_attribute_names
            )
        else:
            if not conditions:
                # If no search criteria were submitted, redirect to the search page
                return None
            condition_str = ' AND '.join(conditions)
            response = table_music.scan(
                # IndexName='year-title-artist-index',
                FilterExpression=condition_str,
                ExpressionAttributeValues=values,
            )

        # No matches
        if not response['Items']:
            return None

        # Matches found
        items = []
        for item in response['Items']:
            artist_name = item['artist'].strip().replace(' ', '')
            artist_image_url = get_image(artist_name, api=True)
            # add the image URL to the item dictionary
            item['image_url'] = artist_image_url
            # add the item dictionary to the list of items
            items.append(item)

        # Return items with 'image_url' field
        return items

