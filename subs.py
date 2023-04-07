import boto3
import requests
import json
import uuid

def get_subscriptions(email, dynamodb, api=False):
    if api:
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
        pass
    else:
        table_subscriptions = dynamodb.Table('subscriptions')
        # query the DynamoDB table for items with the matching email
        response = table_subscriptions.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        subscriptions = []
        s3 = boto3.client('s3')
        for item in response['Items']:
            artist_name = item['artist'].strip().replace(' ', '')
            img_url = s3.generate_presigned_url('get_object', Params={'Bucket': 's3491222-test', 'Key': f'{artist_name}.jpg'})
            subscription = item
            subscription['img_url'] = img_url
            subscriptions.append(subscription)

        return subscriptions

def subscribe_new(email, title, artist, year, dynamodb, api=False):
    if api:
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

    else:
        subscription_id = str(uuid.uuid4())
        table_subscriptions = dynamodb.Table('subscriptions')

        # insert a new row into the subscription table
        table_subscriptions.put_item(
            Item={
                'subscription_id': subscription_id,
                'email': email,
                'title': title,
                'artist': artist,
                'year': year
            }
        )
        return True

def unsubscribe_music(email, subscription_id, dynamodb, api=False):
    if api:
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

    else:
        table_subscriptions = dynamodb.Table('subscriptions')
        # delete item from subscription table
        table_subscriptions.delete_item(
            Key={
                'subscription_id': subscription_id,
                'email': email
            }
        )
        return True


# def get_subscriptions():
#     email = session['email']
#     # query the DynamoDB table for items with the matching email
#     response = table_subscriptions.query(
#         KeyConditionExpression='email = :email',
#         ExpressionAttributeValues={':email': email}
#     )

#     # extract the items from the response and return as a JSON array
#     items = response['Items']
#     serialized_items = []
#     for item in items:
#         serialized_item = {}
#         for key in item:
#             serialized_item[key] = list(item[key].values())[0]
#         serialized_items.append(serialized_item)
#     print('Serialized Items:')
#     print(serialized_items)
#     pass