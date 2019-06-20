import csv
import time
import urllib.request, json
from datetime import datetime
import math

with open ('forum_address_type2.csv') as csv_file:
    url = ''
    transaction_no = ''
    transactions = []
    data_dict = {}
    for row in csv_file:
        transactions = []
        addr = row.split(',')[0]
        url = 'https://blockchain.info/rawaddr/' + addr
        time.sleep(1)
        with urllib.request.urlopen(url) as new_url:
            data = new_url.read()
            data_dict = json.loads(data)
            transaction_no = data_dict['n_tx']
        num_rounds = math.ceil(transaction_no/50)
        for i in range(num_rounds):
            offset = '?offset=' + str(50*i)
            url = 'https://blockchain.info/rawaddr/' + addr + offset
            print(url)
            time.sleep(1)
            with urllib.request.urlopen(url) as new_url:
                data = new_url.read()
                data_dict = json.loads(data)
                transactions += data_dict['txs']

        times = []
        times.append(addr)
        for tx in transactions:
            ts = int(tx['time'])
            dtime = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            times.append(dtime)
        print(times)
        
        with open('txs.csv', 'a', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(times)
