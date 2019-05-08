import json
import requests
import time
import pymysql

def requ(url):
    flag = True
    while flag:
        try:
            result = json.loads(requests.get(url, timeout=3).text)
            flag = False
            return result
        except:
            flag = True
            time.sleep(1)

def craw():
    url = 'https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=usdt-btc'

    send_list = []

    order_5 = []
    order_30 = []
    order_60 = []
    order_300 = []
    order_900 = []
    order_1800 = []

    length5 = 0
    length30 = 0
    length60 = 0
    length300 = 0
    length900 = 0
    length1800 = 0

    result = requ(url)['result']
    result.reverse()

    open_5 = result[-1]['Price']
    close_5 = result[-1]['Price']
    high_5 = result[-1]['Price']
    low_5 = result[-1]['Price']
    volume_5 = result[-1]['Quantity']

    open_30 = result[-1]['Price']
    close_30 = result[-1]['Price']
    high_30 = result[-1]['Price']
    low_30 = result[-1]['Price']
    volume_30 = result[-1]['Quantity']

    open_60 = result[-1]['Price']
    close_60 = result[-1]['Price']
    high_60 = result[-1]['Price']
    low_60 = result[-1]['Price']
    volume_60 = result[-1]['Quantity']

    open_300 = result[-1]['Price']
    close_300 = result[-1]['Price']
    high_300 = result[-1]['Price']
    low_300 = result[-1]['Price']
    volume_300 = result[-1]['Quantity']

    open_900 = result[-1]['Price']
    close_900 = result[-1]['Price']
    high_900 = result[-1]['Price']
    low_900 = result[-1]['Price']
    volume_900 = result[-1]['Quantity']

    open_1800 = result[-1]['Price']
    close_1800 = result[-1]['Price']
    high_1800 = result[-1]['Price']
    low_1800 = result[-1]['Price']
    volume_1800 = result[-1]['Quantity']

    time_num5 = 3
    time_num30 = 15
    time_num60 = 30
    time_num300 = 150
    time_num900 = 450
    time_num1800 = 900

    history_id = []
    history_oder = []

    db = pymysql.connect("localhost", "root", "lq88255503", "qtsm")
    cursor = db.cursor()
    mysql_number = 0

    id5 = 0
    id30 = 0
    id60 = 0
    id300 = 0
    id900 = 0
    id1800 = 0
    while True:
        result = requ(url)['result']
        result.reverse()
        for i in result:
            if i['Id'] not in history_id:
                if (i['Price'] < low_5):
                    low_5 = i['Price']
                if (i['Price'] < low_30):
                    low_30 = i['Price']
                if (i['Price'] < low_60):
                    low_60 = i['Price']
                if (i['Price'] < low_1800):
                    low_1800 = i['Price']
                if (i['Price'] < low_900):
                    low_900 = i['Price']
                if (i['Price'] < low_300):
                    low_300 = i['Price']

                if (i['Price'] > high_5):
                    high_5 = i['Price']
                if (i['Price'] > high_30):
                    high_30 = i['Price']
                if (i['Price'] > high_60):
                    high_60 = i['Price']
                if (i['Price'] > high_300):
                    high_300 = i['Price']
                if (i['Price'] > high_900):
                    high_900 = i['Price']
                if (i['Price'] > high_1800):
                    high_1800 = i['Price']

                volume_5 += i['Quantity']
                volume_30 += i['Quantity']
                volume_60 += i['Quantity']
                volume_300 += i['Quantity']
                volume_900 += i['Quantity']
                volume_1800 += i['Quantity']

                history_id.append(i['Id'])
                history_oder.append(i)
                sql = "INSERT INTO historid(historyorder,historyid) VALUES ('%s','%s')" % (json.dumps(i),i['Id'])
                cursor.execute(sql)
                db.commit()

                length5 += 1
                length30 += 1
                length60 += 1
                length300 += 1
                length900 += 1
                length1800 += 1

        if(len(order_5)>3000):
            for k in range(10):
                order_5.pop(k)
        if (len(order_30) > 3000):
            for k in range(10):
                order_30.pop(k)
        if (len(order_60) > 3000):
            for k in range(10):
                order_60.pop(k)
        if (len(order_300) > 3000):
            for k in range(10):
                order_300.pop(k)
        if (len(order_900) > 3000):
            for k in range(10):
                order_900.pop(k)
        if (len(order_1800) > 3000):
            for k in range(10):
                order_1800.pop(k)
        if(len(history_id)>3000):
            for i in range(1000):
                history_id.pop(i)
                history_oder.pop(i)

        if (time_num5 >= 5) and (length5 >= 3):
            close_5 = result[-1]['Price']
            sql = "INSERT INTO order_test5(valuess) VALUES ('%s')" % (json.dumps({'open': open_5, 'close': close_5, 'high': high_5, 'low': low_5,
                                                   'volume': volume_5}))
            cursor.execute(sql)
            low_5 = result[-1]['Price']
            high_5 = result[-1]['Price']
            open_5 = result[-1]['Price']
            volume_5 = result[-1]['Quantity']
            time_num5 = 0
            length5 = 0
            id5 += 1

        if (time_num30 >= 30) and (length30 >= 6):
            close_30 = result[-1]['Price']
            sql = "INSERT INTO order_test30(valuess) VALUES ('%s')" % (
            json.dumps({'open': open_30, 'close': close_30, 'high': high_30, 'low': low_30,
                                                   'volume': volume_30}))
            cursor.execute(sql)
            low_30 = result[-1]['Price']
            high_30 = result[-1]['Price']
            open_30 = result[-1]['Price']
            volume_30 = result[-1]['Quantity']
            time_num30 = 0
            length30 = 0
            id30 += 1

        if (time_num60 >= 60) and (length60 >= 12):
            close_60 = result[-1]['Price']
            sql = "INSERT INTO order_test60(valuess) VALUES ('%s')" % (
            json.dumps({'open': open_60, 'close': close_60, 'high': high_60, 'low': low_60,
                                                   'volume': volume_60}))
            cursor.execute(sql)
            low_60 = result[-1]['Price']
            high_60 = result[-1]['Price']
            open_60 = result[-1]['Price']
            volume_60 = result[-1]['Quantity']
            time_num60 = 0
            length60 = 0
            id60 += 1

        if (time_num300 >= 300) and (length300 >= 20):
            close_300 = result[-1]['Price']
            sql = "INSERT INTO order_test300(valuess) VALUES ('%s')" % (
            json.dumps({'open': open_300, 'close': close_300, 'high': high_300, 'low': low_300,
                                                   'volume': volume_300}))
            cursor.execute(sql)
            low_300 = result[-1]['Price']
            high_300 = result[-1]['Price']
            open_300 = result[-1]['Price']
            volume_300 = result[-1]['Quantity']
            time_num300 = 0
            length300 = 0
            id300 += 1

        if (time_num900 >= 900) and (length900 >= 30):
            close_900 = result[-1]['Price']
            sql = "INSERT INTO order_test900(valuess) VALUES ('%s')" % (
            json.dumps({'open': open_900, 'close': close_900, 'high': high_900, 'low': low_900,
                                                   'volume': volume_900}))
            cursor.execute(sql)
            low_900 = result[-1]['Price']
            high_900 = result[-1]['Price']
            open_900 = result[-1]['Price']
            volume_900 = result[-1]['Quantity']
            time_num900 = 0
            length900 = 0
            id900 += 1

        if (time_num1800 >= 1800) and (length1800 >= 50):
            close_1800 = result[-1]['Price']
            sql = "INSERT INTO order_test5(valuess) VALUES ('%s')" % (
            json.dumps({'open': open_1800, 'close': close_1800, 'high': high_1800, 'low': low_1800,
                                                   'volume': volume_1800}))
            cursor.execute(sql)
            low_1800 = result[-1]['Price']
            high_1800 = result[-1]['Price']
            open_1800 = result[-1]['Price']
            volume_1800 = result[-1]['Quantity']
            time_num1800 = 0
            length1800 = 0
            id1800 += 1

        db.commit()

        time_num5 += 1
        time_num30 += 1
        time_num60 += 1
        time_num300 += 1
        time_num900 += 1
        time_num1800 += 1

        time.sleep(1)
        mysql_number += 1
        if(mysql_number == 30000):
            db = pymysql.connect("localhost", "root", "lq88255503", "qtsm")
            cursor = db.cursor()

craw()