import json
import datetime
import pymysql

from kaishare_utils import *
from pytz import timezone


def execute(sql, flag=False):
    with db.cursor() as cursor:
        cursor.execute(sql)
        if flag:
            result = cursor.fetchall()
            db.commit()
            return result
        db.commit()
        return None


def close(user, p_id):
    try:
        sql1 = f"""SELECT m_id, p_status FROM post WHERE p_id = {p_id};"""
        post = execute(sql1, True)[0]
        poster = post[0]
        status = post[1]

        if status != 'active':
            return (400, "This event is already closed.")

        if user != poster:
            return (400, "Only poster can close the event.")

        sql2 = f"""UPDATE post SET p_status = 'closed' WHERE p_id = {p_id};"""
        execute(sql2)

        result = (200, "Closing Successed.")

    except Exception as e:
        print("Error : ", e)
        result = (400, "Closing failed.")

    return result


def lambda_handler(event, context):
    try:
        event = parse_event(event)
        user, tk, res = check_token(event)
        if res['statusCode'] != 200:
            print("Response : ", res)
            return res

        global db
        db = pymysql.connect(host='kaishare-db.c61emr7whdod.ap-northeast-2.rds.amazonaws.com',
                            port=3306, user='admin', passwd='team7800', db='KAIshare', charset='utf8')

        p_id = int(event['p_id'])

        sc, dt = close(user, p_id)
        result = create_response(event, sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(event, 500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result