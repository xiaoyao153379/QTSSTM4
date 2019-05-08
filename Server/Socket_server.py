from socket import *
from multiprocessing import Process
import pymysql
import json

server=socket(AF_INET,SOCK_STREAM)
server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
server.bind(('127.0.0.1',8080))
server.listen(5)

def sendli(cursor,conn,order_test,number):
    li = []
    sql = 'select count(*) from ' + order_test
    cursor.execute(sql)
    number = cursor.fetchall()[0][0]
    sql = 'select * from '+order_test+' where id > %s' % (number - number)
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        print(i)
        li.append(json.loads(i[1]))
    conn.send(json.dumps(li))

def talk(conn,client_addr):
    db = pymysql.connect("localhost", "root", "12345678", "qtsm")
    cursor = db.cursor()

    conn.send('please input password:\n')

    msg = conn.recv(1024)

    if(msg == '123456'):
        while True:
            try:
                msg = conn.recv(1024)
                if not msg: break
                if (msg == '5'):
                    sendli(cursor,conn,'order_test5',3000)
                elif (msg == '30'):
                    sendli(cursor,conn,'order_test30',3000)
                elif (msg == '60'):
                    sendli(cursor,conn,'order_test60',3000)
                elif (msg == '300'):
                    sendli(cursor,conn,'order_test300',3000)
                elif (msg == '900'):
                    sendli(cursor,conn,'order_test900',3000)
                elif (msg == '1800'):
                    sendli(cursor,conn,'order_test1800',3000)
                elif (msg == 'historyid'):
                    sendli(cursor, conn, 'historid', 2000)
                conn.send(msg.upper())
            except Exception:
                break
    else:
        conn.send('gun')
        conn.close()



if __name__ == '__main__':
    while True:
        conn,client_addr=server.accept()
        p=Process(target=talk,args=(conn,client_addr))
        p.start()
