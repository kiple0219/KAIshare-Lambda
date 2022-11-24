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


def post_info(p_id):
    try:
        sql1 = f"""SELECT p_nickname, p_title, p_content, p_status, p_product, \
                p_capacity, p_joins, p_time, p_place, p_price, p_upload \
                FROM post WHERE p_id = {p_id};"""
        post = execute(sql1, True)[0]

        res_dic = {
            'nickname': post[0], 'title': post[1], 'content': post[2], 'status': post[3],
            'product': post[4], 'capacity': post[5], 'joins': post[6], 'time': str(post[7]),
            'place': post[8], 'price': post[9], 'upolad': str(post[10]), 'comments':[]
        }

        sql2 = f"""SELECT c_id, c_nickname, c_content, c_upload FROM comment WHERE p_id = {p_id};"""
        comments = execute(sql2, True)

        for comment in comments:
            com_dic = {
                'c_id': str(comment[0]), 'nickname': comment[1], 'content': comment[2], 'upload': str(comment[3])
            }
            res_dic['comments'].append(com_dic)
        
        result = (200, res_dic)

    except Exception as e:
        print("Error : ", e)
        result = (400, "Loading post information failed.")

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

        sc, dt = post_info(p_id)
        result = create_response(sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result