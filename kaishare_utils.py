import json
import jwt
import datetime


def parse_event(event):
    print("Unparsed Event : ", event)

    cookie, origin = "", "https://localhost:3000"
    if 'origin' in event['headers']:
        origin = event['headers']['origin']
    if 'Cookie' in event['headers']:
        cookie = event['headers']['Cookie']
    elif 'cookie' in event['headers']:
        cookie = event['headers']['cookie']

    result = {"Cookie": cookie, "origin": origin}

    if event['body']:
        result.update(json.loads(event['body']))
    if event['queryStringParameters']:
        result.update(event['queryStringParameters'])
    if event['pathParameters']:
        result.update(event['pathParameters'])
    
    print("Parsed Event : ", result)
    return result


def create_response(event, statuscode, data, token=''):
    origin = event['origin']
    return {
            "statusCode" : statuscode, 
            "headers": {
                        "Access-Control-Allow-Headers": "Content-Type", 
                        "Access-Control-Allow-Origin": origin,
                        "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PATCH,PUT", 
                        "Access-Control-Allow-Credentials": "true", 
                        "Set-Cookie": "Token=" + token + '; Path=/; HttpOnly; SameSite=None; Secure;'
                        }, 
            "body": json.dumps(data)
            }


def check_token(event):
    cookie_dic = {}
    cookie = event['Cookie']
    cookies = cookie.split('; ')

    for c in cookies:
        c = c.split('=')
        cookie_dic[c[0]] = c[1]

    token = cookie_dic['Token']
    user = ""

    try:
        check = jwt.decode(token, 'cs350team7800', algorithms = "HS256")
        
        user = check['token']['id']
        t_iat = check['token']['iat']

        current_time = datetime.datetime.now()
        token_time = datetime.datetime.strptime(t_iat, "%Y-%m-%d %H:%M:%S.%f")

        token_age = (current_time-token_time).seconds
        print(f"User Info : {user} used the application {str(token_age)} seconds")

        if token_age >= 36000:
            result = create_response(event, 401, "Token has expired over time.")

        elif token_age >= 18000:
            payload = {
                'id': user,
                'iat': str(current_time),
            }
            token = jwt.encode({"token": payload}, 'cs350team7800', algorithm = "HS256")
            result = create_response(event, 200, {"id": user, "Authorization": token})

        else:
            result = create_response(event, 200, {"id": user, "Authorization": ""}, token)

    except Exception as e:
        print("Exception Occured :", e)
        result = create_response(event, 401, "Incorrect Token.")
    
    return user, token, result