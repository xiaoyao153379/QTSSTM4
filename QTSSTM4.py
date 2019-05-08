from CRAW.craw import craw
from multiprocessing import  Pipe,cpu_count,Manager,Process
from BACKTEST.backtest import backtest
from API.api import api
from CANCEL import cancel_order

apikey = ''
manager = Manager()
cpu_count = cpu_count()
order_index = manager.dict()
#########api共享变量
buy_index = manager.list()
sell_index = manager.list()
parent_conn, child_conn = Pipe()
process_list = []
p_backtest = Process(target=backtest,args=(order_index,))
process_list.append(p_backtest)
p_craw = Process(target=craw,args=(order_index, child_conn))
process_list.append(p_craw)
p_api = Process(target=api,args=(parent_conn,buy_index,sell_index))
process_list.append(p_api)
p_cancel = Process(target=cancel_order,args=(apikey))
process_list.append(p_cancel)
for i in process_list:
    i.start()
for i in process_list:
    i.join()