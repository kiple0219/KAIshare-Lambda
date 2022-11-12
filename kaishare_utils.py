import json
import jwt
import datetime


def parse_event(event):
    print("Original Event : ", event)

    result = {"Cookie": ""}
    if 'Cookie' in event['headers']:
        result = {"Cookie": event['headers']['Cookie']}

    if event['body']:
        result.update(json.loads(event['body']))
    if event['queryStringParameters']:
        result.update(event['queryStringParameters'])
    if event['pathParameters']:
        result.update(event['pathParameters'])
    
    print("Parsed Event : ", result)
    return result


def create_response(statuscode, data, token=''):
    return {"statusCode" : statuscode, "body": json.dumps(data), "headers": {"Set-Cookie": token} }


def check_token(event):
    token = event['Cookie']
    token = token.split(' ')[-1]
    user = ""

    try:
        check = jwt.decode(token, 'cs350team7800', algorithms = "HS256")
        
        user = check['token']['id']
        t_iat = check['token']['iat']

        current_time = datetime.datetime.now()
        token_time = datetime.datetime.strptime(t_iat, "%Y-%m-%d %H:%M:%S.%f")

        token_age = (current_time-token_time).seconds
        print(f"User Info : {user} used the application {str(token_age)} seconds")

        if token_age >= 3600 :
            result = create_response(401, "Token has expired over time.")

        elif token_age >= 1800:
            payload = {
                'id': user,
                'iat': str(current_time),
            }
            token = jwt.encode({"token": payload}, 'cs350team7800', algorithm = "HS256")
            result = create_response(200, {"id": user, "Authorization": token})

        else:
            result = create_response(200, {"id": user, "Authorization": ""}, token)

    except Exception as e:
        print("Exception Occured :", e)
        result = create_response(401, "Incorrect Token.")
    
    return user, token, result