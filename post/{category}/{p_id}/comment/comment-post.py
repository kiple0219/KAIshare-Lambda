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


def comment_post(user, p_id, nick, content):
    now = datetime.datetime.now(timezone("Asia/Seoul"))
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    content = content.replace("\'", "\''")

    try:
        sql1 = f"""INSERT INTO comment SET m_id = '{user}', p_id = {p_id}, c_nickname = '{nick}', 
        c_content = '{content}', c_upload = '{now}';"""
        execute(sql1)
        result = (200, "Comment Uploading Successed.")

    except Exception as e:
        print("Error : ", e)
        result = (400, "Comment Uploading failed.")

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
        nick, content = event['nickname'], event['content']

        sc, dt = comment_post(user, p_id, nick, content)
        result = create_response(sc, dt, tk)
        
    except Exception as e:
        print("Error : ", e)
        result = create_response(500, "Internal server error occured.", tk)
    
    
    print("Response : ", result)
    return result