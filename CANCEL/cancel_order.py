import requests
import pymysql
import json
import time

def cancel(key):
    db = pymysql.connect("localhost", "root", "password", "qtsm")
    cursor = db.cursor()
    mysql_number = 0
    while True:
        sql = "SELECT * FROM order_table"
        cursor.execute(sql)
        result = cursor.fetchall()
        if (len(result) != 0):
            for i in result:
                if (i[3] == 30):
                    judge(key,i[1],i[2],db,cursor)
                    sql = "DELETE FROM order_table WHERE uid = '%s'" % (i[1])
                    cursor.execute(sql)
                else:
                    sql = "UPDATE order_table SET timess = %s WHERE uid = '%s'" % (
                        str(i[3] + 1), i[1])
                    cursor.execute(sql)

            db.commit()
        time.sleep(1)
        if(mysql_number > 30000):
            db = pymysql.connect("localhost", "root", "password", "qtsm")
            cursor = db.cursor()
            mysql_number = 0

def urls(url):
    while flag:
        try:
            result = json.loads(requests.get(url, timeout=3).text)['result']
            flag = False
            return result
        except:
            flag = True
            time.sleep(1)

def judge(key,uid,value,db,cursor):
    flag = True
    url = 'https://api.bittrex.com/api/v1.1/market/getopenorders?apikey=' + key + '&market=USDT-BTC'
    url_cancel = 'https://api.bittrex.com/api/v1.1/market/cancel?apikey=' + key + '&uuid='
    result = urls()

    if(len(result) == 0):
        pass
    else:
        for i in result:
            if(uid == i):
                result = urls(url_cancel+uid)
                print(result.text)
                sql = "INSERT INTO funding(funding, uid) VALUES ('%s', '%s',)" % (value, uid)
                cursor.execute(sql)
                db.commit()


