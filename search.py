import os
import json
import boto3

client = boto3.client('s3')
result = client.get_object(
    Bucket=os.environ['SEARCH_S3_BUCKET'],
    Key='search.json'
)
search_all = json.loads(result["Body"].read().decode('utf-8'))

def search(event, context):
    # Filter out from search_all into a new object and format it as Semantic UI needs
    body = {
        'random': "Some Random Crap"
    }
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, ensure_ascii=False, separators=(',', ':')),
        'isBase64Encoded': False
    }


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    print(
        search(
            event={
                'resource': '/shows/search/{query}',
                'path': '/shows/search/Breaking B',
                'httpMethod': 'GET',
                'headers': None,
                'queryStringParameters': None,
                'pathParameters': {
                    'query': 'Breaking B'
                },
                'stageVariables': None,
                'requestContext': {
                    'path': '/shows/search/{query}',
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
                    'resourcePath': '/shows/search/{query}',
                    'httpMethod': 'GET',
                    'apiId': 'abcdefghij'
                },
                'body': None,
                'isBase64Encoded': False
            },
            context=None
        )
    )
