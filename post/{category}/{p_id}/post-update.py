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


def post_update(p_id, user, nick, title, content, product, capacity, time, place, price):
    try:
        sql1 = f"""SELECT m_id, p_status FROM post WHERE p_id = {p_id};"""
        post = execute(sql1, True)[0]
        poster = post[0]
        status = post[1]

        if poster != user:
            return(400, "Only poster can edit the event.")
        if status != "active":
            return(400, "Only active event can edit.")

        sql2 = f"""UPDATE post SET m_id = '{user}', p_nickname = '{nick}', p_title = '{title}', \
                p_content = '{content}', p_product = '{product}', p_capacity = {capacity}, \
                p_time = '{time}', p_place = '{place}', p_price = {price} WHERE p_id = {p_id};"""
        execute(sql2)

        result = (200, "Post Update Successed.")

    except Exception as e:
        print("Error : ", e)
        result = (400, "Post Update failed.")

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
        nick, title, content, product = event['nickname'], event['title'], event['content'], event['product']
        capacity, time, place, price = event['capacity'], event['time'], event['place'], event['price']

        sc, dt = post_update(p_id, user, nick, title, content, product, capacity, time, place, price)
        result = create_response(event, sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(event, 500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result