import numpy as np
import talib
import random
from multiprocessing import  Pool,Pipe,cpu_count,Manager


def ma(order, buy_index, sell_index,rate,args):
    close = []
    for i in order:
        close.append(i['close'])
    close = np.array(close)
    result = talib.MA(close, timeperiod=int(args))
    result = [float(x) for x in result]
    if(result[-1] > close[-1]):
        buy_index.append(float(rate))
    elif(result[-1] < close[-1]):
        sell_index.append(float(rate))
    else:
        pass
    print('2')

'''li = []
for i in range(1000):
    li.append({'open': random.uniform(1000, 2000), 'close': random.uniform(1000, 2000), 'high': random.uniform(2000, 3000), 'low':  random.uniform(0, 1000), 'volume': random.uniform(10, 20)})
print(li)
pool = Pool(processes=2)
pool.apply_async(func=cmo,args=(li,[],[],15,13))
pool.close()
pool.join()'''

