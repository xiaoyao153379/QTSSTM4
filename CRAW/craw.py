import json
import requests
import time
import socket
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

def returnli(cursor,order_test,number):
    li = []
    sql = 'SELECT * FROM '+order_test+' order by id desc limit '+number
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        li.append(json.loads(i[1]))
    li.reverse()
    return li

def craw(order_index,child_conn):
    url = 'https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=usdt-btc'

    host = '00.00.00.00'
    send_list = []
    history_id = []

    db = pymysql.connect(host, "root", "password", "qtsm")
    cursor = db.cursor()

    order_5 = returnli(cursor,'order_test5','2000')
    order_30 = returnli(cursor, 'order_test30', '1200')
    order_60 = returnli(cursor, 'order_test60', '1000')
    order_300 = returnli(cursor, 'order_test300', '500')
    order_900 = returnli(cursor, 'order_test900', '300')
    order_1800 = returnli(cursor, 'order_test1800', '200')
    history_id = returnli(cursor,'historid','800')

    order_index['order5'] = order_5
    order_index['order30'] = order_30
    order_index['order60'] = order_60
    order_index['order300'] = order_300
    order_index['order900'] = order_900
    order_index['order1800'] = order_1800

    cursor.close()
    db.close()

    for i in order_5[-90:-1]:
        send_list.append({'action':'5','value':i})
    send_list.append({'action':'5','value':order_5[-1]})

    for i in order_30[-90:-1]:
        send_list.append({'action':'30','value':i})
    send_list.append({'action': '30', 'value': order_30[-1]})

    for i in order_60[-90:-1]:
        send_list.append({'action':'60','value':i})
    send_list.append({'action': '60', 'value': order_60[-1]})

    for i in order_300[-90:-1]:
        send_list.append({'action':'300','value':i})
    send_list.append({'action': '300', 'value': order_300[-1]})

    for i in order_900[-90:-1]:
        send_list.append({'action':'900','value':i})
    send_list.append({'action': '900', 'value': order_900[-1]})

    if(len(order_1800)>0):
        for i in order_1800[-90:-1]:
            send_list.append({'action': '1800', 'value': i})
        send_list.append({'action': '1800', 'value': order_1800[-1]})

    child_conn.send(send_list)

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
    time_num60 = 60
    time_num300 = 150
    time_num900 = 450
    time_num1800 = 900

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
                history_id.pop(i)

        if (time_num5 >= 5) and (length5 >= 20):
            close_5 = result[-1]['Price']
            order_5.append({'open': open_5, 'close': close_5, 'high': high_5, 'low': low_5,
                                                   'volume': volume_5})
            order_index['order5'] = order_5

            send_list.append({'action': '5', 'value': {'open': open_5, 'close': close_5, 'high': high_5, 'low': low_5,
                                                      'volume': volume_5}})

            low_5 = result[-1]['Price']
            high_5 = result[-1]['Price']
            open_5 = result[-1]['Price']
            volume_5 = result[-1]['Quantity']
            time_num5 = 0
            length5 = 0

        if (time_num30 >= 5) and (length30 >= 30):
            close_30 = result[-1]['Price']
            order_30.append({'open': open_30, 'close': close_30, 'high': high_30, 'low': low_30,
                                                   'volume': volume_30})
            order_index['order30'] = order_30
            send_list.append({'action': '30', 'value': {'open': open_30, 'close': close_30, 'high': high_30, 'low': low_30,
                                                   'volume': volume_30}})
            low_30 = result[-1]['Price']
            high_30 = result[-1]['Price']
            open_30 = result[-1]['Price']
            volume_30 = result[-1]['Quantity']
            time_num30 = 0
            length30 = 0

        if (time_num60 >= 60) and (length60 >= 40):
            close_60 = result[-1]['Price']
            order_60.append({'open': open_60, 'close': close_60, 'high': high_60, 'low': low_60,
                                                   'volume': volume_60})
            order_index['order60'] = order_60
            send_list.append({'action': '60', 'value': {'open': open_60, 'close': close_60, 'high': high_60, 'low': low_60,
                                                   'volume': volume_60}})
            low_60 = result[-1]['Price']
            high_60 = result[-1]['Price']
            open_60 = result[-1]['Price']
            volume_60 = result[-1]['Quantity']
            time_num60 = 0
            length60 = 0

        if (time_num300 >= 300) and (length300 >= 50):
            close_300 = result[-1]['Price']
            order_300.append({'open': open_300, 'close': close_300, 'high': high_300, 'low': low_300,
                                                   'volume': volume_300})
            order_index['order300'] = order_300
            send_list.append({'action': '300', 'value': {'open': open_300, 'close': close_300, 'high': high_300, 'low': low_300,
                                                   'volume': volume_300}})
            low_300 = result[-1]['Price']
            high_300 = result[-1]['Price']
            open_300 = result[-1]['Price']
            volume_300 = result[-1]['Quantity']
            time_num300 = 0
            length300 = 0

        if (time_num900 >= 900) and (length900 >= 60):
            close_900 = result[-1]['Price']
            order_900.append({'open': open_900, 'close': close_900, 'high': high_900, 'low': low_900,
                                                   'volume': volume_900})
            order_index['order900'] = order_900
            send_list.append({'action': '900', 'value': {'open': open_900, 'close': close_900, 'high': high_900, 'low': low_900,
                                                   'volume': volume_900}})
            low_900 = result[-1]['Price']
            high_900 = result[-1]['Price']
            open_900 = result[-1]['Price']
            volume_900 = result[-1]['Quantity']
            time_num900 = 0
            length900 = 0

        if (time_num1800 >= 1800) and (length1800 >= 70):
            close_1800 = result[-1]['Price']
            order_1800.append({'open': open_1800, 'close': close_1800, 'high': high_1800, 'low': low_1800,
                                                   'volume': volume_1800})
            order_index['order1800'] = order_1800
            send_list.append({'action': '1800', 'value': {'open': open_1800, 'close': close_1800, 'high': high_1800, 'low': low_1800,
                                                   'volume': volume_1800}})
            low_1800 = result[-1]['Price']
            high_1800 = result[-1]['Price']
            open_1800 = result[-1]['Price']
            volume_1800 = result[-1]['Quantity']
            time_num1800 = 0
            length1800 = 0

        if(len(send_list) != 0):
            child_conn.send(send_list)
            del send_list[:]

        time_num5 += 1
        time_num30 += 1
        time_num60 += 1
        time_num300 += 1
        time_num900 += 1
        time_num1800 += 1

        time.sleep(1)
