import boto3
import zlib
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GraphTV-Ratings-Prod')


def get_ratings(event, context):
    print(event)
    response = table.get_item(
        Key={
            'id': event['pathParameters']['showId']
        }
    )
    # Return Base64-encoded ZLIB binary data (1x execution time)
    # return {'ratings': base64.b64encode(response['Item']['data'].value).decode('utf-8')}
    #
    # Return decompressed JSON data (415x execution time)
    # return json.loads(zlib.decompress(response['Item']['data'].value).decode())
    #return {'data': base64.b64encode(response['Item']['data'].value).decode('utf-8')}
    return {
        'statusCode': 200,
        'headers': {
            'x-custom-header': 'my custom header value'
        },
        'body': zlib.decompress(response['Item']['data'].value).decode(),
        'isBase64Encoded': False
    }


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    get_ratings({"id": "tt0903747"}, None)
    #get_ratings({"id": "tt0058796"}, None)
