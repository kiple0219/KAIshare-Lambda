import json
import datetime
import pymysql

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


def signin(id, pw, phone):
    mail = id.split('@')[-1]
    if mail != "kaist.ac.kr":
        return (400, "Id is not kaist mail.")

    sql1 = f"""SELECT count(*) FROM member WHERE m_id = '{id}';"""
    user = execute(sql1, True)

    if user[0][0] > 0:
        result = (401, "Id is already exist")

    else:
        sql2 = f"""INSERT INTO member SET m_id = '{id}', m_password = '{pw}', m_phone = '{phone}';"""
        execute(sql2)

        result = (200, f"Signin Successed.")

    return result


def lambda_handler(event, context):
    try:
        event = parse_event(event)
        global db
        db = pymysql.connect(host='kaishare-db.c61emr7whdod.ap-northeast-2.rds.amazonaws.com',
                            port=3306, user='admin', passwd='team7800', db='KAIshare', charset='utf8')

        id, pw, phone = event['id'], event['password'], event['phone']

        sc, dt = signin(id, pw, phone)
        result = create_response(event, sc, dt)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(event, 500, "Internal server error occured.")
    
    
    print("Response : ", result)
    return result