import talib
from PARTMEMBER.start_end import *
import numpy as np
from POSITIONMANAGE.bk_position import bk_position
import operator
import pymysql
import random
from multiprocessing import  Pool,Pipe,cpu_count,Manager

def pysql_connect():
    db = pymysql.connect("localhost", "root", "12345678", "qtsm")
    cursor = db.cursor()
    return {'db':db,'cursor':cursor}

def ma(judge_position, buy_amount, sell_amount, coin_number, principal, order, period):
    profit_loss = {}

    pyrsult = pysql_connect()
    db = pyrsult['db']
    cursor = pyrsult['cursor']

    close_list = []
    for i in order:
        close_list.append(i['close'])

    init_princpal = coin_number * close_list[0] + principal

    close = np.array(close_list)

    for timeperiod in range(ma_start, ma_end):
        trade_index = []

        result = talib.MA(close, timeperiod=timeperiod)
        result_ma = [float(x) for x in result]

        for i in range(len(result_ma)):
            if (result_ma[i] > close_list[i]):
                trade_index.append(1)
            elif (result_ma[i] < close_list[i]):
                trade_index.append(-1)
            else:
                trade_index.append(0)

        posit_result = bk_position(buy_amount, sell_amount, coin_number, principal, judge_position, trade_index,
                                   close_list)

        last_princpal = posit_result['last_princle']
        trade_number = posit_result['trade_number']

        if (trade_number == 0):
            profit_loss[str(timeperiod)] = 0
        else:
            result_trade = last_princpal - init_princpal
            profit_loss[str(timeperiod)] = result_trade / trade_number
    sorsult = sorted(profit_loss.items(), key=operator.itemgetter(1), reverse=True)[0]

    sql = "UPDATE k%s SET args = '%s' WHERE function_name = '%s'" % (str(period), str(sorsult[0]), 'ma')
    sql1 = "UPDATE k%s SET rate_trade = '%s' WHERE function_name = '%s'" % (str(period), str(sorsult[1]), 'ma')

    cursor.execute(sql)
    cursor.execute(sql1)

    db.commit()
    cursor.close()
    db.close()

'''li = []
for i in range(1000):
    li.append({'open': random.uniform(1000, 2000), 'close': random.uniform(1000, 2000), 'high': random.uniform(2000, 3000), 'low':  random.uniform(0, 1000), 'volume': random.uniform(10, 20)})
print(li)
pool = Pool(processes=2)
pool.apply_async(func=ultosc,args=(0.5,1000,1000,15,100000,li,5))
pool.close()
pool.join()'''






