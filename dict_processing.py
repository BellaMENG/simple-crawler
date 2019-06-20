import pickle
intervals = [1, 7, 10, 15, 20, 25, 30, 35, 40, 45, 50]

with open('transactions_dict.pickle', 'rb') as f1:
    datetime_dict = pickle.load(f1)

with open('posts_dict.pickle', 'rb') as f2:
    post_dict = pickle.load(f2)

for interval in intervals:
    count = 0
    for addr in datetime_dict.keys():
        # 86400
        plus = False
        post_times = post_dict[addr]
        transaction_times = datetime_dict[addr]
        for t1 in post_times:
            for t2 in transaction_times:
                if (t2 > t1):
                    dt_diff = t2 - t1
                    dt_diff_in_days = dt_diff.total_seconds()/86400
                    if dt_diff_in_days <= interval:
                        plus = True
        if plus:
            count += 1

    print("for an interval of " + str(interval) + " days, " + str(count) + " out of " + str(len(datetime_dict.keys())) + " users have transaction after any of their posts")

