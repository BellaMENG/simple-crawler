import csv
import time
import urllib.request, json
from datetime import datetime
import math
import mysql.connector
from mysql.connector import pooling
import pickle

interval = 7
datetime_dict = {}
post_dict = {}

print("getting transaction time: ")
with open ('demo.csv') as csv_file:
    for row in csv_file:
        datetimes = []
        addr = row.split(',')[0]
        dates = row.split(',')[1:]
        print(addr)
        for d in dates:
            if len(d) == 19:
                datetime_obj = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
                datetimes.append(datetime_obj)
        datetime_dict[addr] = datetimes
print("getting post time: ")
c1 = 0
for addr in datetime_dict.keys():
    c1 += 1
    if c1 % 10 == 0:
        print(c1)
    dts = []
    connection_pool = pooling.MySQLConnectionPool(pool_name = 'bitforum',
                                                  host = 'bmz708.ust.hk',
                                                  database = 'bitforum',
                                                  user = 'yiyang',
                                                  password = 'yiyang')
    connection_object = connection_pool.get_connection()
    
    cursor = connection_object.cursor()
    sql = "select post_time from post where user_id in (select distinct user_id from user_entity_t where entity_id in (select entity_id from address_entity where address = \'" + addr + "\')) order by post_time desc;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for r in results:
        dts.append(r[0])
    post_dict[addr] = dts
    if (connection_object.is_connected()):
        cursor.close()
        connection_object.close()

print("dicts done")

with open('transactions_dict.pickle', 'wb') as f1:
    pickle.dump(datetime_dict, f1)
with open('posts_dict.pickle', 'wb') as f2:
    pickle.dump(post_dict, f2)

count = 0
post_times = []
for addr in datetime_dict.keys():
# 86400
    plus = False
    post_times = post_dict[addr]
    transaction_times = datetime_dict[addr]
    for t1 in post_times:
        print('a')
        for t2 in transaction_times:
            if (t2 > t1) and ((t2 - t1)/86400 <= interval):
                plus = True
    if plus:
        count += 1

print(str(count) + '/' + str(c1))


