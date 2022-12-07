import json

def lambda_handler(event, context):
    origin = ''
    if 'origin' in event['headers']:
        origin = event['headers']['origin']
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers": "x-api-key, Content-Type",
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true',
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PATCH,PUT,DELETE"
        },
    }