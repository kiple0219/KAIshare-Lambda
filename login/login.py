import json
import datetime
import pymysql
import jwt

from kaishare_utils import *


def execute(sql, flag=False):
    with db.cursor() as cursor:
        cursor.execute(sql)
        if flag:
            result = cursor.fetchall()
            db.commit()
            return result
        db.commit()
        return None


def login(id, pw):
    sql1 = f"""SELECT m_password FROM member WHERE m_id = '{id}';"""
    user = execute(sql1, True)

    if len(user) == 0:
        result = (401, "User is not exist.", "")
    
    elif pw != user[0][0]:
        result = (401, "Password is not correct.", "")

    else:
        payload = {
            'id': id,
            'iat': str(datetime.datetime.now())
        }
        token = jwt.encode({"token": payload}, "cs350team7800", algorithm = "HS256")
        result = (200, f"Welcome {id}!", token)

    return result


def lambda_handler(event, context):
    try:
        event = parse_event(event)
        global db
        db = pymysql.connect(host='kaishare-db.c61emr7whdod.ap-northeast-2.rds.amazonaws.com',
                            port=3306, user='admin', passwd='team7800', db='KAIshare', charset='utf8')

        id, pw = event['id'], event['password']

        sc, dt, tk = login(id, pw)
        result = create_response(event, sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(event, 500, "Internal server error occured.")
    
    
    print("Response : ", result)
    return result