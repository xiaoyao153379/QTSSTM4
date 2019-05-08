import pymysql
from STRATEGY.api_strategy import *
from multiprocessing import  Pool,Pipe,cpu_count,Manager
from POSITIONMANAGE.api_position import api_position
import json
import time

def call(number):
    print(number)

def pysql_connect():
    db = pymysql.connect("localhost", "root", "12345678", "qtsm")
    cursor = db.cursor()
    return {'db':db,'cursor':cursor}

def return_data(cursor,table_name):
    di = {}
    sql = "SELECT * FROM " + table_name
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        di[i[1]] = {'args':i[2],'rate_trade':i[3]}
    return di

def api(parent_conn,buy_index,sell_index):

    time.sleep(5)

    current_price = 0

    trade_signal = {'5':{'buy_index':0,'sell_index':0},'30':{'buy_index':0,'sell_index':0},'60':{'buy_index':0,'sell_index':0},'300':{'buy_index':0,'sell_index':0},'900':{'buy_index':0,'sell_index':0},'1800':{'buy_index':0,'sell_index':0}}

    judge_position = 0.5  # 仓位比
    buy_amount = 1000
    sell_amount = 1000
    coin_number = 0
    principal = 100000

    principal30 = principal / 6
    principal60 = principal / 6
    principal300 = principal / 6
    principal900 = principal / 6
    principal1800 = principal / 6
    principal5 = principal / 6

    init_principal30 = principal / 6
    init_principal60 = principal / 6
    init_principal300 = principal / 6
    init_principal900 = principal / 6
    init_principal1800 = principal / 6
    init_principal5 = principal / 6

    coin_number5 = coin_number /6
    coin_number30 = coin_number / 6
    coin_number60 = coin_number / 6
    coin_number300 = coin_number / 6
    coin_number900= coin_number / 6
    coin_number1800 = coin_number / 6

    mysql_result = pysql_connect()

    db = mysql_result['db']
    cursor = mysql_result['cursor']
    period_dict = {}

    mysql_number = 0
    recv = parent_conn.recv()

    order5 = []
    order30 = []
    order60 = []
    order300 = []
    order900 = []
    order1800 = []

    for i in recv:
        if (i['action'] == '5'):
            order5.append(i['value'])
        if (i['action'] == '30'):
            order30.append(i['value'])
        if (i['action'] == '60'):
            order60.append(i['value'])
        if (i['action'] == '300'):
            order300.append(i['value'])
        if (i['action'] == '900'):
            order900.append(i['value'])
        if (i['action'] == '1800'):
            order1800.append(i['value'])

    len_order5 = 0
    len_order30 = 0
    len_order60 = 0
    len_order300 = 0
    len_order900 = 0
    len_order1800 = 0

    while True:
        period_dict['5'] = return_data(cursor, 'k5')
        period_dict['30'] = return_data(cursor, 'k30')
        period_dict['60'] = return_data(cursor, 'k60')
        period_dict['300'] = return_data(cursor, 'k300')
        period_dict['900'] = return_data(cursor, 'k900')
        period_dict['1800'] = return_data(cursor, 'k1800')
        recv = parent_conn.recv()
        sql = "SELECT * FROM funding"
        cursor.execute(sql)
        data = cursor.fetchall()


        if(len(data) == 0):
            pass
        else:
            for j in data:
                value = json.loads(j[1])

                uid = j[2]

                last_price = value['current_price']

                value = value['result']

                for i in value:
                    if (i == '5'):
                        if (i['action'] == 'buy'):
                            principal5 += i['buy_amount']
                            coin_number5 -= i['buy_amount'] / last_price
                        else:
                            principal5 -= i['sell_amount']
                            coin_number5 += i['sell_amount'] / last_price
                    if (i == '30'):
                        if (i['action'] == 'buy'):
                            principal30 += i['buy_amount']
                            coin_number30 -= i['buy_amount'] / last_price
                        else:
                            principal30 -= i['sell_amount']
                            coin_number30 += i['sell_amount'] / last_price
                    if (i == '60'):
                        if (i['action'] == 'buy'):
                            principal60 += i['buy_amount']
                            coin_number60 -= i['buy_amount'] / last_price
                        else:
                            principal60 -= i['sell_amount']
                            coin_number60 += i['sell_amount'] / last_price
                    if (i == '300'):
                        if (i['action'] == 'buy'):
                            principal300 += i['buy_amount']
                            coin_number300 -= i['buy_amount'] / last_price
                        else:
                            principal300 -= i['sell_amount']
                            coin_number300 += i['sell_amount'] / last_price
                    if (i == '900'):
                        if (i['action'] == 'buy'):
                            principal900 += i['buy_amount']
                            coin_number900 -= i['buy_amount'] / last_price
                        else:
                            principal900 -= i['sell_amount']
                            coin_number900 += i['sell_amount'] / last_price
                    if (i == '1800'):
                        if (i['action'] == 'buy'):
                            principal1800 += i['buy_amount']
                            coin_number1800 -= i['buy_amount'] / last_price
                        else:
                            principal1800 -= i['sell_amount']
                            coin_number1800 += i['sell_amount'] / last_price
                sql = "DELETE FROM funding WHERE uid = '%s'" % (uid)
                cursor.execute(sql)
            db.commit()

        for i in recv:
            if(i['action'] == '5'):
                order5.append(i['value'])
            if (i['action'] == '30'):
                order30.append(i['value'])
            if (i['action'] == '60'):
                order60.append(i['value'])
            if (i['action'] == '300'):
                order300.append(i['value'])
            if (i['action'] == '900'):
                order900.append(i['value'])
            if (i['action'] == '1800'):
                order1800.append(i['value'])

        current_price = i['value']['close']

        print('current_price:'+str(current_price))

        if(len(order5) > 100) and (len(order5) != len_order5):
            pool = Pool(processes=(4))
            if (float(period_dict['5']['ma']['rate_trade']) > 0):
                pool.apply_async(func=ma, args=(
                order5, buy_index, sell_index, period_dict['5']['ma']['rate_trade'], period_dict['5']['ma']['args']))
            pool.close()
            pool.join()
            for i in buy_index:
                trade_signal['5']['buy_index'] = trade_signal['5']['buy_index'] + i
            for i in sell_index:
                trade_signal['5']['sell_index'] = trade_signal['5']['sell_index'] + i
            del buy_index[:]
            del sell_index[:]
            len_order5 = len(order5)
        if (len(order30) > 100) and (len(order30) != len_order30):
            pool = Pool(processes=(4))
            if (float(period_dict['30']['ma']['rate_trade']) > 0):
                pool.apply_async(func=ma, args=(
                order30, buy_index, sell_index, period_dict['30']['ma']['rate_trade'], period_dict['30']['ma']['args']))
            pool.close()
            pool.join()
            for i in buy_index:
                trade_signal['30']['buy_index'] = trade_signal['30']['buy_index'] + i
            for i in sell_index:
                trade_signal['30']['sell_index'] = trade_signal['30']['sell_index'] + i
            del buy_index[:]
            del sell_index[:]
            len_order30 = len(order30)
        if (len(order60) > 100) and (len(order60) != len_order60):
            pool = Pool(processes=(3))
            if (float(period_dict['60']['ma']['rate_trade']) > 0):
                pool.apply_async(func=ma, args=(
                order60, buy_index, sell_index, period_dict['60']['ma']['rate_trade'], period_dict['60']['ma']['args']))
            pool.close()
            pool.join()
            for i in buy_index:
                trade_signal['60']['buy_index'] = trade_signal['60']['buy_index'] + i
            for i in sell_index:
                trade_signal['60']['sell_index'] = trade_signal['60']['sell_index'] + i
            del buy_index[:]
            del sell_index[:]
            len_order60 = len(order60)
        if (len(order300) > 100) and (len(order300) != len_order300):
            pool = Pool(processes=(3))
            if (float(period_dict['300']['ma']['rate_trade']) > 0):
                pool.apply_async(func=ma, args=(order300, buy_index, sell_index, period_dict['300']['ma']['rate_trade'],
                                                period_dict['300']['ma']['args']))
            pool.close()
            pool.join()
            for i in buy_index:
                trade_signal['300']['buy_index'] = trade_signal['300']['buy_index'] + i
            for i in sell_index:
                trade_signal['300']['sell_index'] = trade_signal['300']['sell_index'] + i
            del buy_index[:]
            del sell_index[:]
            len_order300 = len(order300)
        if (len(order900) > 100) and (len(order900) != len_order900):
            pool = Pool(processes=(3))
            if (float(period_dict['900']['ma']['rate_trade']) > 0):
                pool.apply_async(func=ma, args=(order900, buy_index, sell_index, period_dict['900']['ma']['rate_trade'],
                                                period_dict['900']['ma']['args']))
            pool.close()
            pool.join()
            for i in buy_index:
                trade_signal['900']['buy_index'] = trade_signal['900']['buy_index'] + i
            for i in sell_index:
                trade_signal['900']['sell_index'] = trade_signal['900']['sell_index'] + i
            del buy_index[:]
            del sell_index[:]
            len_order900 = len(order900)
        if (len(order1800) > 100) and (len(order1800) != len_order1800):
            pool = Pool(processes=(3))
            if (float(period_dict['1800']['ma']['rate_trade']) > 0):
                pool.apply_async(func=ma, args=(
                order1800, buy_index, sell_index, period_dict['1800']['ma']['rate_trade'],
                period_dict['1800']['ma']['args']))
            pool.close()
            pool.join()
            for i in buy_index:
                trade_signal['1800']['buy_index'] = trade_signal['1800']['buy_index'] + i
            for i in sell_index:
                trade_signal['1800']['sell_index'] = trade_signal['1800']['sell_index'] + i
            del buy_index[:]
            del sell_index[:]
            len_order1800 = len(order1800)


        temp = {}

        for i in trade_signal:
            if(trade_signal[i]['buy_index'] == 0) and (trade_signal[i]['sell_index'] == 0):
                pass
            else:
                temp[i] = trade_signal[i]

        if(len(temp)>0):
            result = api_position(db,cursor,temp,principal5,principal30,principal60,principal300,principal900,principal1800,coin_number5,coin_number30,coin_number60,coin_number300,coin_number900,coin_number1800,judge_position,sell_amount,buy_amount,current_price)
            print(result)
            principal30 = result['principal30']
            principal60 = result['principal60']
            principal300 = result['principal300']
            principal900 = result['principal900']
            principal1800 = result['principal1800']
            principal5 = result['principal5']

            coin_number5 = result['coin_number5']
            coin_number30 = result['coin_number30']
            coin_number60 = result['coin_number60']
            coin_number300 = result['coin_number300']
            coin_number900 = result['coin_number900']
            coin_number1800 = result['coin_number1800']

        mysql_number += 1

        if (mysql_number > 30000):
            mysql_result = pysql_connect()

            db = mysql_result['db']
            cursor = mysql_result['cursor']
            period_dict = {}
            mysql_number = 0

        lats_principal = principal5 + principal1800 + principal900 + principal300 + principal30 + principal60 + (
                coin_number5 + coin_number30 + coin_number60 + coin_number300 + coin_number900 + coin_number1800) * current_price
        print('principal: ' + str(lats_principal))

        print('loss_profit:' + str(lats_principal - principal))

        print('principal5:' + str(principal5) + ':coin_number5:' + str(coin_number5) + ':loss_profit:' + str(
            principal5 + current_price * coin_number5 - init_principal5))

        print('principal1800:' + str(principal1800) + ':coin_number1800:' + str(
            coin_number1800) + ':loss_profit:' + str(
            principal1800 + current_price * coin_number1800 - init_principal1800))

        print(
            'principal900:' + str(principal900) + ':coin_number900:' + str(coin_number900) + ':loss_profit:' + str(
                principal900 + current_price * coin_number900 - init_principal900))

        print(
            'principal300:' + str(principal300) + ':coin_number300:' + str(coin_number300) + ':loss_profit:' + str(
                principal300 + current_price * coin_number300 - init_principal300))

        print('principal30:' + str(principal30) + ':coin_number30:' + str(coin_number30) + ':loss_profit:' + str(
            principal30 + current_price * coin_number30 - init_principal30))

        print('principal60:' + str(principal60) + ':coin_number60:' + str(coin_number60) + ':loss_profit:' + str(
            principal60 + current_price * coin_number60 - init_principal60))

        db.commit()
        trade_signal = {'5': {'buy_index': 0, 'sell_index': 0}, '30': {'buy_index': 0, 'sell_index': 0},
                    '60': {'buy_index': 0, 'sell_index': 0}, '300': {'buy_index': 0, 'sell_index': 0},
                    '900': {'buy_index': 0, 'sell_index': 0}, '1800': {'buy_index': 0, 'sell_index': 0}}





