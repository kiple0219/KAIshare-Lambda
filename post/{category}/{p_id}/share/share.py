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


def share(user, p_id):
    try:
        sql1 = f"""SELECT p_status FROM post WHERE p_id = {p_id};"""
        post = execute(sql1, True)[0]

        if post[0] != 'closed':
            return(400, "Only closed event can see the information.")

        sql2 = f"""SELECT m_id, m_phone FROM joining natural join member WHERE p_id = {p_id};"""
        members = execute(sql2, True)

        res_list = []
        check = False
        for member in members:
            if member[0] == user:
                check = True
            res_dic = {'id': member[0], 'phone': member[1]}
            res_list.append(res_dic)
            
        if not check:
            return (400, "Only joining members can see the infomation.")
        
        result = (200, res_list)

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

        sc, dt = share(user, p_id)
        result = create_response(sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result