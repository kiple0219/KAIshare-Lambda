import json
import datetime
import jwt
from kaishare_utils import *


def lambda_handler(event, context):
    
    try:
        event = parse_event(event)
        name = event['name']
        payload = {
            'id': name,
            'iat': str(datetime.datetime.now()),
        }
        
        token = jwt.encode({"token": payload}, "cs350team7800", algorithm = "HS256")
        kk = {"Cookie": token}
        parse, res = check_token(kk)
        
        result = create_response(200, f"hello {name}!", parse)
        
    except Exception as e:
        result = create_response(400, str(e), parse)
    
    
    print("Response : ", result)
    return result