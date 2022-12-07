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


def join(user, p_id):
    try:
        sql1 = f"""SELECT p_capacity, p_joins, p_status FROM post WHERE p_id = {p_id};"""
        post = execute(sql1, True)[0]
        capacity = post[0]
        joins = post[1]
        status = post[2]

        if joins >= capacity:
            return (400, "This event is fulled.")
        elif status != 'active':
            return (400, "This event is closed.")

        sql2 = f"""SELECT m_id FROM joining WHERE p_id = {p_id};"""
        joiners = execute(sql2, True)

        for joiner in joiners:
            if joiner[0] == user:
                return (400, "You already joined the event.")

        joins += 1
        sql3 = f"""INSERT INTO joining SET p_id = {p_id}, m_id = '{user}';"""
        sql4 = f"""UPDATE post SET p_joins = {joins} WHERE p_id = {p_id};"""
        execute(sql3)
        execute(sql4)

        result = (200, "Joining Successed.")

    except Exception as e:
        print("Error : ", e)
        result = (400, "Joining failed.")

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

        sc, dt = join(user, p_id)
        result = create_response(event, sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(event, 500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result