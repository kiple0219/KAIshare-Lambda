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


def leave(user, p_id):
    try:
        sql1 = f"""SELECT p_joins, p_status, m_id FROM post WHERE p_id = {p_id};"""
        post = execute(sql1, True)[0]
        joins = post[0] - 1
        status = post[1]
        poster = post[2]

        if status != 'active':
            return (400, "This event is closed.")
        
        if user == poster:
            return (400, "Poster can't leave the event.")

        sql1 = f"""SELECT m_id FROM joining WHERE p_id = {p_id};"""
        joiners = execute(sql1, True)
        check = False
        for joiner in joiners:
            if joiner[0] == user:
                check = True
        
        if check:
            sql3 = f"""DELETE FROM joining WHERE p_id = {p_id} and m_id = '{user}';"""
            sql4 = f"""UPDATE post SET p_joins = {joins} WHERE p_id = {p_id};"""
            execute(sql3)
            execute(sql4)

            result = (200, "Leaving Successed.")

        else:
            result = (400, "You didn't join the event.")

    except Exception as e:
        print("Error : ", e)
        result = (400, "Leaving failed.")

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
        sc, dt = leave(user, p_id)
        result = create_response(sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result