import boto3
import zlib
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['RATINGS_TABLE'])


def get_ratings(event, context):
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
    # return {'data': base64.b64encode(response['Item']['data'].value).decode('utf-8')}
    #
    # May need to fix the Header here to be different depending on the API Gateway settings.
    # Solution would be to add a API Gateway Stage Variable with the info and it will be
    # passed in the request, which we just reference here.
    if response['Item']['data'].value[:1] == '{':
        # If this is straight JSON
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': response['Item']['data'].value,
            'isBase64Encoded': False
        }
    else:
        # If it doesn't begin with '{' then it is compressed
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': zlib.decompress(response['Item']['data'].value).decode(),
            'isBase64Encoded': False
        }


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    print(
        get_ratings(
            event={
                'resource': '/shows/{showId}/ratings',
                'path': '/shows/3N6z/ratings',
                'httpMethod': 'GET',
                'headers': None,
                'queryStringParameters': None,
                'pathParameters': {
                    'showId': '3N6z'
                },
                'stageVariables': None,
                'requestContext': {
                    'path': '/shows/{showId}/ratings',
                    'accountId': '123456789012',
                    'resourceId': 'abcdef',
                    'stage': 'test-invoke-stage',
                    'requestId': 'test-invoke-request',
                    'identity': {
                        'cognitoIdentityPoolId': None,
                        'cognitoIdentityId': None,
                        'apiKey': 'test-invoke-api-key',
                        'cognitoAuthenticationType': None,
                        'userArn': 'arn:aws:iam::123456789012:user/GraphTV',
                        'apiKeyId': 'test-invoke-api-key-id',
                        'userAgent': 'Apache-HttpClient/4.5.x (Java/1.8.0_144)',
                        'accountId': '123456789012',
                        'caller': 'CALLERABCDEFGHIJKLMNO',
                        'sourceIp': 'test-invoke-source-ip',
                        'accessKey': 'ACCESSKEYZYXWVUTSRQP',
                        'cognitoAuthenticationProvider': None,
                        'user': 'USERABCDEFGHIJKLMNOPQ'
                    },
                    'resourcePath': '/shows/{showId}/ratings',
                    'httpMethod': 'GET',
                    'apiId': 'abcdefghij'
                },
                'body': None,
                'isBase64Encoded': False
            },
            context=None
        )
    )
