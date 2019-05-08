from multiprocessing import  Pool,Pipe,cpu_count,Manager
from pandas import DataFrame
import numpy as np
import operator
from STRATEGY.bk_strategy import *
import pymysql
import time

def pysql_connect():
    db = pymysql.connect("localhost", "root", "12345678", "qtsm")
    cursor = db.cursor()
    return {'db':db,'cursor':cursor}

def call(number):
    pass

def return_data(cursor,table_name):
    di = {}
    sql = "SELECT * FROM " + table_name
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        di[i[1]] = {'args':i[2],'rate_trade':i[3]}
    return di

def init_datebase():
    db = pymysql.connect("localhost", "root", "12345678", "qtsm")
    cursor = db.cursor()
    li = ['ma', 'bbands', 'dmea', 'ema', 'kama', 'midpoint', 'sma', 't3', 'tema', 'trima', 'cmo', 'mom', 'rsi', 'linearreg_angle', 'linearreg_slope', 'linearreg', 'adosc', 'macd', 'ultosc', 'cdl2crows', 'cdl3blackcrows', 'cdl3inside', 'cdl3inestrike', 'cdl3outside', 'cdl3starsinsouth', 'cdl3whitesoldiers', 'cdlabandonedbaby', 'cdlbelthold', 'cdlbreakaway', 'cdlclosingmarubozu', 'cdlconcealbabyswall', 'cdldarkcloudcover', 'cdldojistar', 'cdldragonflydoji', 'cdleveningdojistar', 'cdleveningstar', 'cdlgravestonedoji', 'cdlhammer', 'cdlharami', 'cdlharamicross', 'cdlinneck', 'cdlidentical3crows', 'cdlladderbottom', 'cdlmorningdojistar', 'cdlmorningstar', 'cdlonneck', 'cdlpiercing', 'cdlrisefall3methods', 'cdlshootingstar', 'cdlstalledpattern', 'cdltasukigap', 'cdlxsidegap3methods', 'obv', 'aroon', 'cci', 'mfi', 'willr']
    name = ['5','30','60','300','900','1800']
    for i in name:
        for j in li:
            sql = "UPDATE k%s SET args = '%s' WHERE function_name = '%s'" % (i, '5', j)
            sql1 = "UPDATE k%s SET rate_trade = '%s' WHERE function_name = '%s'" % (
            i, '0', j)
            cursor.execute(sql)
            cursor.execute(sql1)
    db.commit()
    cursor.close()
    db.close()

def backtest(order_index):
    init_datebase()
    order_index['order5'] = []
    order_index['order30'] = []
    order_index['order60'] = []
    order_index['order300'] = []
    order_index['order900'] = []
    order_index['order1800'] = []

    judge_position = 0.5  # 仓位比
    buy_amount = 1000
    sell_amount = 1000
    coin_number = 0
    principal = 100000

    order5 = order_index['order5']
    order30 = order_index['order30']
    order60 = order_index['order60']
    order300 = order_index['order300']
    order900 = order_index['order900']
    order1800 = order_index['order1800']

    len_order5 = len(order5)
    len_order30 = len(order30)
    len_order60 = len(order60)
    len_order300 = len(order300)
    len_order900 = len(order900)
    len_order1800 = len(order1800)

    while True:
        order5 = order_index['order5']
        order30 = order_index['order30']
        order60 = order_index['order60']
        order300 = order_index['order300']
        order900 = order_index['order900']
        order1800 = order_index['order1800']
        if ((len(order5) > 1200) and (len(order5) != len_order5)):
            pool = Pool(processes=(3))
            pool.apply_async(func=ma, args=(
            judge_position, buy_amount, sell_amount, coin_number, principal, order5, 5),callback=call(1))
            pool.close()
            pool.join()
            len_order5 = len(order5)
        if ((len(order30) > 800) and (len(order30) != len_order30)):
            pool = Pool(processes=(3))
            pool.apply_async(func=ma, args=(
            judge_position, buy_amount, sell_amount, coin_number, principal, order30, 30),callback=call(1))
            pool.close()
            pool.join()
            len_order30 = len(order30)
        if ((len(order60) > 600) and (len(order60) != len_order60)):
            pool = Pool(processes=(3))
            pool.apply_async(func=ma, args=(
            judge_position, buy_amount, sell_amount, coin_number, principal, order60, 60),callback=call(1))
            pool.close()
            pool.join()
            len_order60 = len(order60)
        if ((len(order300) > 400) and (len(order300) != len_order300)):
            pool = Pool(processes=(3))
            pool.apply_async(func=ma, args=(
            judge_position, buy_amount, sell_amount, coin_number, principal, order300, 300),callback=call(1))
            pool.close()
            pool.join()
            len_order300 = len(order300)
        if ((len(order900) > 300) and (len(order900) != len_order900)):
            pool = Pool(processes=(3))
            pool.apply_async(func=ma, args=(
            judge_position, buy_amount, sell_amount, coin_number, principal, order900, 900),callback=call(1))
            pool.close()
            pool.join()
            len_order900 = len(order900)
        if ((len(order1800) > 200) and (len(order1800) != len_order1800)):
            pool = Pool(processes=(3))
            pool.apply_async(func=ma, args=(
            judge_position, buy_amount, sell_amount, coin_number, principal, order1800, 1800),callback=call(1))
            pool.close()
            pool.join()
            len_order1800 = len(order1800)

