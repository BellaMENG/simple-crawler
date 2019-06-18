import csv
import time
import urllib.request, json

with open ('forum_address_type2.csv') as csv_file:
    url = ''
    transaction_no = ''
    for row in csv_file:
        addr = row.split(',')[0]
        url = 'https://blockchain.info/rawaddr/' + addr
        time.sleep(2)
        with urllib.request.urlopen(url) as new_url:
            data = new_url.read()
            data_dict = json.loads(data)
            transaction_no = data_dict['n_tx']
        csv_row = [addr, transaction_no]
        print(csv_row)
        with open('n_tx.csv', 'a', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow([csv_row[0], csv_row[1]])
