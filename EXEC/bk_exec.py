

def Exec(trade_signal, price, coin_number, principal, buy_amount, sell_amount):
    if (trade_signal == 'buy'):
        if (buy_amount > principal):
            principal = 0
            coin_number += (principal / price)
        else:
            coin_number += (buy_amount / price)
            principal -= buy_amount
    elif (trade_signal == 'sell'):
        if ((sell_amount / price) > coin_number):
            coin_number = 0
            principal += coin_number * price
        else:
            coin_number -= (sell_amount / price)
            principal += sell_amount
    else:
        pass
    return {'coin_number': coin_number, 'principal': principal}