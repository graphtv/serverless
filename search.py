import os
import json
import boto3
import urllib
from collections import OrderedDict

client = boto3.client('s3')
result = client.get_object(
    Bucket=os.environ['SEARCH_S3_BUCKET'],
    Key='search.json'
)
show_list = json.loads(result["Body"].read().decode('utf-8'))


def search(event, context):
    # https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
    search_term = urllib.parse.unquote(event['pathParameters']['query']).casefold()
    raw_results = [curShow for curShow in show_list if search_term in curShow['t'].casefold()]
    results = sorted(raw_results, key=lambda k: k['v'], reverse=True)
    # May need to fix the Header here to be different depending on the API Gateway settings.
    # Solution would be to add a API Gateway Stage Variable with the info and it will be
    # passed in the request, which we just reference here.
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'results': results[0:7]}, ensure_ascii=False, separators=(',', ':')),
        'isBase64Encoded': False
    }


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    print(
        search(
            event={
                "body": None,
                "headers": {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "CloudFront-Forwarded-Proto": "https",
                    "CloudFront-Is-Desktop-Viewer": "true",
                    "CloudFront-Is-Mobile-Viewer": "false",
                    "CloudFront-Is-SmartTV-Viewer": "false",
                    "CloudFront-Is-Tablet-Viewer": "false",
                    "CloudFront-Viewer-Country": "US",
                    "Host": "REDACTED-HOSTNAME",
                    "Referer": "http://REDACTED-HOSTNAME/",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)...",
                    "Via": "2.0 abc.cloudfront.net (CloudFront)",
                    "X-Amz-Cf-Id": "a__b-c",
                    "X-Amzn-Trace-Id": "Root=1-abc",
                    "X-Forwarded-For": "1.2.3.4, 5.6.7.8",
                    "X-Forwarded-Port": "443",
                    "X-Forwarded-Proto": "https",
                    "cache-control": "no-cache",
                    "origin": "http://REDACTED-HOSTNAME",
                    "pragma": "no-cache"
                },
                "httpMethod": "GET",
                "isBase64Encoded": False,
                "path": "/search/Breaking%20B",
                "pathParameters": {
                    "query": "Break"
                },
                "queryStringParameters": None,
                "requestContext": {
                    "accountId": "123456789012",
                    "apiId": "abcdefghij",
                    "httpMethod": "GET",
                    "identity": {
                        "accessKey": None,
                        "accountId": None,
                        "caller": None,
                        "cognitoAuthenticationProvider": None,
                        "cognitoAuthenticationType": None,
                        "cognitoIdentityId": None,
                        "cognitoIdentityPoolId": None,
                        "sourceIp": "9.8.7.6",
                        "user": None,
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gec...",
                        "userArn": None
                    },
                    "path": "/search/Breaking%20B",
                    "protocol": "HTTP/1.1",
                    "requestId": "a-b-c-d-e",
                    "requestTime": "13/Jan/2018:07:16:56 +0000",
                    "requestTimeEpoch": 1515827816576,
                    "resourceId": "abcdef",
                    "resourcePath": "/search/{query}",
                    "stage": "live"
                },
                "resource": "/search/{query}",
                "stageVariables": {
                    "environment": "Dev"
                }
            },
            context=None
        )
    )
