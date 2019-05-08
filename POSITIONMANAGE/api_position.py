import json

def api_position(db,cursor,temp,principal5,principal30,principal60,principal300,principal900,principal1800,coin_number5,coin_number30,coin_number60,coin_number300,coin_number900,coin_number1800,judge_position,sell_amount,buy_amount,current_price):
    all_buyamount = 0
    all_sellamount = 0
    trade_amonut = {}
    flee = 0.0025
    for i in temp:
        if(i == '5'):
            trade_amonut['5'] = position(coin_number5,principal5,buy_amount,sell_amount,flee,judge_position,temp[i],current_price)
            if(trade_amonut['5']['action'] == 'buy'):
                principal5 = trade_amonut['5']['value']['principal']
                coin_number5 = trade_amonut['5']['value']['coin_number']
                all_buyamount += trade_amonut['5']['value']['buy_amount']
            if(trade_amonut['5']['action'] == 'sell'):
                principal5 = trade_amonut['5']['value']['principal']
                coin_number5 = trade_amonut['5']['value']['coin_number']
                all_sellamount += trade_amonut['5']['value']['sell_amount']

        if(i == '30'):
            trade_amonut['30'] = position(coin_number30,principal30,buy_amount,sell_amount,flee,judge_position,temp[i],current_price)
            if (trade_amonut['30']['action'] == 'buy'):
                principal30 = trade_amonut['30']['value']['principal']
                coin_number30 = trade_amonut['30']['value']['coin_number']
                all_buyamount += trade_amonut['30']['value']['buy_amount']
            if (trade_amonut['30']['action'] == 'sell'):
                principal30 = trade_amonut['30']['value']['principal']
                coin_number30 = trade_amonut['30']['value']['coin_number']
                all_sellamount += trade_amonut['30']['value']['sell_amount']
        if (i == '60'):
            trade_amonut['60'] = position(coin_number60,principal60,buy_amount,sell_amount,flee,judge_position,temp[i],current_price)
            if (trade_amonut['60']['action'] == 'buy'):
                principal60 = trade_amonut['60']['value']['principal']
                coin_number60 = trade_amonut['60']['value']['coin_number']
                all_buyamount += trade_amonut['60']['value']['buy_amount']
            if (trade_amonut['60']['action'] == 'sell'):
                principal60 = trade_amonut['60']['value']['principal']
                coin_number60 = trade_amonut['60']['value']['coin_number']
                all_sellamount += trade_amonut['60']['value']['sell_amount']
        if (i == '300'):
            trade_amonut['300'] = position(coin_number300,principal300,buy_amount,sell_amount,flee,judge_position,temp[i],current_price)
            if (trade_amonut['300']['action'] == 'buy'):
                principal300 = trade_amonut['300']['value']['principal']
                coin_number300 = trade_amonut['300']['value']['coin_number']
                all_buyamount += trade_amonut['300']['value']['buy_amount']
            if (trade_amonut['300']['action'] == 'sell'):
                principal300 = trade_amonut['300']['value']['principal']
                coin_number300 = trade_amonut['300']['value']['coin_number']
                all_sellamount += trade_amonut['300']['value']['sell_amount']
        if (i == '900'):
            trade_amonut['900'] = position(coin_number900,principal900,buy_amount,sell_amount,flee,judge_position,temp[i],current_price)
            if (trade_amonut['900']['action'] == 'buy'):
                principal900 = trade_amonut['900']['value']['principal']
                coin_number900 = trade_amonut['900']['value']['coin_number']
                all_buyamount += trade_amonut['900']['value']['buy_amount']
            if (trade_amonut['900']['action'] == 'sell'):
                principal900 = trade_amonut['900']['value']['principal']
                coin_number900 = trade_amonut['900']['value']['coin_number']
                all_sellamount += trade_amonut['900']['value']['sell_amount']
        if (i == '1800'):
            trade_amonut['1800'] = position(coin_number1800,principal1800,buy_amount,sell_amount,flee,judge_position,temp[i],current_price)
            if (trade_amonut['1800']['action'] == 'buy'):
                principal1800 = trade_amonut['1800']['value']['principal']
                coin_number1800 = trade_amonut['1800']['value']['coin_number']
                all_buyamount += trade_amonut['1800']['value']['buy_amount']
            if (trade_amonut['1800']['action'] == 'sell'):
                principal1800 = trade_amonut['1800']['value']['principal']
                coin_number1800 = trade_amonut['1800']['value']['coin_number']
                all_sellamount += trade_amonut['1800']['value']['sell_amount']

    if(all_buyamount > all_sellamount):
        uid = exec('buy', all_buyamount - all_sellamount)
        sql = "INSERT INTO order_table(uid , valuess , timess) VALUES ('%s', '%s',  '%s')" % (str(uid), json.dumps(
            {'principal5': principal5, 'coin_number5': coin_number5, 'principal30': principal30,
             'coin_number30': coin_number30, 'principal60': principal60, 'coin_number60': coin_number60,
             'principal300': principal300, 'coin_number300': coin_number300, 'principal900': principal900,
             'coin_number900': coin_number900, 'principal1800': principal1800, 'coin_number1800': coin_number1800,
             'result': trade_amonut, 'current_price': current_price}), 0)
        cursor.execute(sql)
        db.commit()
    if(all_sellamount > all_buyamount):
        uid = exec('sell',all_sellamount-all_buyamount)
        sql = "INSERT INTO order_table(uid , valuess , timess) VALUES ('%s', '%s',  '%s')" % (str(uid), json.dumps(
                {'principal5': principal5, 'coin_number5': coin_number5, 'principal30': principal30,
                 'coin_number30': coin_number30, 'principal60': principal60, 'coin_number60': coin_number60,
                 'principal300': principal300, 'coin_number300': coin_number300, 'principal900': principal900,
                 'coin_number900': coin_number900, 'principal1800': principal1800, 'coin_number1800': coin_number1800,
                 'result': trade_amonut, 'current_price': current_price}), 0)
        cursor.execute(sql)
        db.commit()
    return {'principal5': principal5, 'coin_number5': coin_number5, 'principal30': principal30,
         'coin_number30': coin_number30, 'principal60': principal60, 'coin_number60': coin_number60,
         'principal300': principal300, 'coin_number300': coin_number300, 'principal900': principal900,
         'coin_number900': coin_number900, 'principal1800': principal1800, 'coin_number1800': coin_number1800}

def position(coin_number,principal,buy_amount,sell_amount,flee,judge_position,index,current_price):
    sposition = ( coin_number * current_price ) / (principal + ( coin_number * current_price ))
    if ((index['buy_index'] > index['sell_index']) and (judge_position > sposition)):
        buy_amount2 = (index['buy_index'] / (index['buy_index'] + index['sell_index'])) * buy_amount
        if(buy_amount2 < principal):
            coin_number = ((buy_amount2 - buy_amount2 * flee) / current_price) + coin_number
            principal = principal - buy_amount2
        else:
            buy_amount2 = principal
            coin_number = ((principal - principal * flee) / current_price) + coin_number
            principal = 0
        return {'action':'buy','value':{'buy_amount':buy_amount2,'principal':principal,'coin_number':coin_number}}

    if (index['buy_index'] < index['sell_index'] and (sposition > 0)):
        sell_amount2 = (index['sell_index'] / (index['buy_index'] + index['sell_index'])) * sell_amount
        if((sell_amount2 / current_price) < coin_number):
            coin_number = coin_number - (sell_amount2 / current_price)
            principal = principal + (sell_amount2 - sell_amount2 * flee)
        else:
            sell_amount2 = coin_number * current_price
            principal = principal + (coin_number - coin_number * flee) * current_price
            coin_number = 0
        return {'action':'sell','value': {'sell_amount': sell_amount2, 'principal': principal, 'coin_number': coin_number}}
    return {'action': 'none'}

def exec(action,buy_amount):
    return 23231321