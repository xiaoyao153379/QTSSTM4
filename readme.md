# QTSSTM4

> QTSSTM4 is a quantitative trading system for digital coin.

## Preface

This system is more complex than it, which were released last time. If you are a beginner, you can click the following link. 
* [BakTst_Org](https://github.com/xiaoyao153379/BakTst_Org)
* [BakTst_Trd](https://github.com/xiaoyao153379/BakTst_Trd)
* [scripts](https://github.com/xiaoyao153379/scripts)
## Who is suitable for this software？

* Python programmer

* Quantitative trader

## The special point of this system

* The system will divide principal into six parts, according to the period of time and the number of orders. That is more comprehensive.
* All strategy will experience back test system, and if it earned money, this system uses it at api model.
* You can assign CPU freely by setting the number of "Process.pool". That mean you can set less number of CPU that back test system uses than api, so the back test system will don't use a lot source of CPU.

## How to use it?

**Firstly**, you must set your strategy in "api_strategy" and "bk_strategy". There is some special at the format of the data. For example, ever strategy must be transported these parameters, which are include judge_position, buy_amount, sell_amount, coin_number, principal, order and period.
* judge_position: It is a index of judging position.
* buy_amount: It is a max amount of buying per order.
* sell_amount: It is a max amount of selling per order.
* coin_number: It is your total number of coin.
* principal: It is your principal.
* order: It is data of order. And the format is ```[{'open': open1, 'close': close1, 'high': high1, 'low': low1,'volume': volume1},{'open': open2, 'close': close2, 'high': high2, 'low': low2,'volume': volume2}]```
* period: It is a key of marking table of database.

**Secondly**, you must set database of these system. And you can replace name of table that this system use. And you can find these names in SQL sentence. 
**Finally**, you can control frequency of obtaining data of order at "CRAW". If there is just a little change on price, you can set a low frequency. In contrast, you can set a high frequency.

## In a addition
I have not completed "ordercancel", because it is too simple, and you just need to call api of exchange. Besides, I also have not competed executing order, and it is same as the last. 