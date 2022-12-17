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


def post_post(user, category, nick, title, content, product, capacity, time, place, price):
    now = datetime.datetime.now(timezone("Asia/Seoul"))
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    content = content.replace("\'", "\''")

    try:
        sql1 = f"""INSERT INTO post SET m_id = '{user}', p_nickname = '{nick}', p_title = '{title}', p_content = '{content}',
                p_status = "active", p_category = '{category}', p_product = '{product}', p_capacity = {capacity}, p_joins = 1,
                p_time = '{time}', p_place = '{place}', p_price = {price}, p_upload = '{now}';"""
        execute(sql1)

        sql2 = f"""SELECT p_id FROM post WHERE m_id = '{user}' order by p_id desc"""
        p_id = execute(sql2, True)[0][0]

        sql3 = f"""INSERT INTO joining SET m_id = '{user}', p_id = {p_id};"""
        execute(sql3)
        
        result = (200, "Posting Successed.")

    except Exception as e:
        print("Error : ", e)
        result = (400, "Posting failed.")

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

        category = event['category']
        nick, title, content, product = event['nickname'], event['title'], event['content'], event['product']
        capacity, time, place, price = event['capacity'], event['time'], event['place'], event['price']

        if nick == '':
            nick = "Unknown"
        if title == '':
            title = "No Title"
        if product == '':
            product = "TBD"
        if place == '':
            place = "TBD"

        sc, dt = post_post(user, category, nick, title, content, product, capacity, time, place, price)
        result = create_response(event, sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(event, 500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result