import json

from kaishare_utils import *

def lambda_handler(event, context):
    event = parse_event(event)
    
    try:
        result = create_response(event, 200, "Logout Successed.")

    except Exception as e:
        print("Error : ", e)
        result = create_response(event, 500, "Internal server error occured.")

    return result