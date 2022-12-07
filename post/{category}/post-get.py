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


def post_get(category, nickname, title, content, product, place, status, capacity, price, time_from, time_to):
    sql1 = f"""SELECT p_id, p_nickname, p_title, p_status, p_upload FROM post \
            WHERE p_category = '{category}' and p_status <> 'disable' \
            and p_nickname like '%{nickname}%' and p_title like '%{title}%' \
            and p_content like '%{content}%' and p_product like '%{product}%' \
            and p_place like '%{place}%' and p_status like '%{status}%' \
            and p_capacity <= {capacity} and p_price <= {price} \
            and p_time >= '{time_from}' and p_time <= '{time_to}'order by p_id desc;"""

    try:
        posts = execute(sql1, True)
        res_list = []
        
        for post in posts:
            res_dic = {
                'p_id': str(post[0]), 'nickname': post[1], 'title': post[2], 
                'status': post[3], 'upolad': str(post[4])
            }
            res_list.append(res_dic)
        
        result = (200, res_list)

    except Exception as e:
        print("Error : ", e)
        result = (400, "Loading posts failed.")

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
        nickname, title, content, product, place, status = '', '', '', '', '', ''
        capacity, price = 1000, 10000000
        time_from, time_to = '1999-01-01', '2999-01-01'

        if 'nickname' in event:
            nickname = event['nickname']
        if 'title' in event:
            title = event['title']
        if 'content' in event:
            content = event['content']
        if 'product' in event:
            product = event['product']
        if 'place' in event:
            place = event['place']
        if 'status' in event:
            status = event['status']
        if 'capacity' in event:
            capacity = event['capacity']
        if 'price' in event:
            price = event['price']
        if 'time_from' in event:
            time_from = event['time_from']
        if 'time_to' in event:
            time_to = event['time_to']

        sc, dt = post_get(category, nickname, title, content, product, place, status, capacity, price, time_from, time_to)
        result = create_response(event, sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(event, 500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result