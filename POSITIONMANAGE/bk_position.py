from EXEC.bk_exec import Exec


def bk_position(buy_amount,sell_amount,coin_number,principal,judge_position,trade_index,close_list):
    position = ( coin_number * close_list[0] ) / (principal + ( coin_number * close_list[0] ))
    trade_number = 0
    li = []
    for i in range(len(trade_index)):
        if((trade_index[i] > 0) and (judge_position > position)):
            trade_signal = 'buy'
            result_Exec = Exec(trade_signal, close_list[i], coin_number, principal, buy_amount, sell_amount)
            coin_number = result_Exec['coin_number']
            principal = result_Exec['principal']
            if(coin_number == 0) and (principal == 0):
                return {'last_princle':0,'trade_number':trade_number}
            position = (coin_number * close_list[i]) / (principal + (coin_number * close_list[i]))
            trade_number += 1

        elif ((trade_index[i] < 0) and (position > 0)):
            trade_signal = 'sell'
            result_Exec = Exec(trade_signal, close_list[i], coin_number, principal, buy_amount, sell_amount)
            coin_number = result_Exec['coin_number']
            principal = result_Exec['principal']
            if (coin_number == 0) and (principal == 0):
                return {'last_princle': 0, 'trade_number': trade_number}
            position = (coin_number * close_list[i]) / (principal + (coin_number * close_list[i]))
            trade_number += 1
        else:
            pass
        li.append((principal))
    last_princle = close_list[-1] * coin_number + principal
    return {'last_princle':last_princle,'trade_number':trade_number}