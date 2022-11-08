import json

def create_response(statuscode, data):
    return {"statusCode" : statuscode, "body": json.dumps(data)}
    
def parse_event(event):
    print(event)
    result = {}
    
    if event['queryStringParameters']:
        result.update(event['queryStringParameters'])
    if event['pathParameters']:
        result.update(event['pathParameters'])

    return result


def lambda_handler(event, context):
    event = parse_event(event)
    
    try:
        name = event['name']
        result = create_response(200, f"hello {name}")
        
    except Exception as e:
        result = create_response(400, "There is no name!")
    
    return result