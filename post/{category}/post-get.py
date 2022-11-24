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


def post_get(category, type, keyword):
    if type == 'all':
        sql1 = f"""SELECT p_id, p_nickname, p_title, p_status, p_upload FROM post \
                WHERE p_category = '{category}' and p_status <> 'disable' order by p_id desc;"""

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
        type, keyword = event['type'], event['keyword']

        sc, dt = post_get(category, type, keyword)
        result = create_response(sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result