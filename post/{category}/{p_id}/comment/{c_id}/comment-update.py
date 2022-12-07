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


def comment_update(user, c_id, nick, content):
    content = content.replace("\'", "\''")

    try:
        sql1 = f"""SELECT m_id FROM comment WHERE c_id = {c_id};"""
        comment = execute(sql1, True)[0]
        poster = comment[0]

        if poster != user:
            return (400, "Commented User is Different.")

        sql2 = f"""UPDATE comment SET c_nickname = '{nick}', c_content = '{content}' WHERE c_id = {c_id};"""
        execute(sql2)
        result = (200, "Comment Update Successed.")

    except Exception as e:
        print("Error : ", e)
        result = (400, "Comment Update Failed.")

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

        c_id = int(event['c_id'])
        nick, content = event['nickname'], event['content']

        sc, dt = comment_update(user, c_id, nick, content)
        result = create_response(event, sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(event, 500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result