import requests
import json
import boto3

def get_image(artist_name, api=False):
    if api:
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
        pass
    else:
        s3 = boto3.client('s3')
        artist_image_url = s3.generate_presigned_url('get_object', Params={'Bucket': 's3491222-test', 'Key': f'{artist_name}.jpg'})
        return artist_image_url

    


# def get_image(item):
#     try:
#         artist_name = item['artist'].strip().replace(' ', '')
#         img_url = s3.generate_presigned_url('get_object', Params={'Bucket': 's3491222-test', 'Key': f'{artist_name}.jpg'})
#         print(img_url)
#         return img_url

#     except:
#         return jsonify({'error': 'Image not found'}), 404
