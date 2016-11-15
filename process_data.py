import pandas as pd
import numpy as np
import convert_time
import csv
import time

def slimify():
    with open('long_ideas.csv', 'r') as file:
        with open('long_ideas_slim.csv', 'w') as w_file:
            reader = csv.reader(file, delimiter = ',')
            writer = csv.writer(w_file, delimiter = ',')
            header = True
            for row in reader:
                if header is True:
                    header = False
                    writer.writerow((row[0], row[1], row[2], row[3]))
                    #print "%s,%s,%s,%s" % (row[0], row[1], row[2], row[3])
                    continue

                article_id = row[0]
                stock_ticker = row[1]
                link = row[2]
                date = convert_time.convert_time(row[3])
                if date is None:
                    continue
                #print "%s,%s,%s,%s" % (article_id, stock_ticker, link, date)
                writer.writerow((article_id, stock_ticker, link, date))

def combine():
    ideas_dict = {}
    with open('long_ideas_slim.csv', 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        header = True
        count = 1
        for row in reader:
            #print row
            if header is True:
                header = False
                continue
            if row[3] not in ideas_dict:
                ideas_dict[row[3]] = []
                tickers = row[1].split(',')
                for ticker in tickers:
                    clean_ticker = ticker.strip()
                    ideas_dict[row[3]].append(clean_ticker)
            else:
                tickers = row[1].split(',')
                for ticker in tickers:
                    clean_ticker = ticker.strip()
                    if clean_ticker not in ideas_dict[row[3]]:
                        ideas_dict[row[3]].append(clean_ticker)
            count += 1

    with open('long_ideas_out.csv', 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        count = 1
        total = len(ideas_dict)
        for key in ideas_dict:
            writer.writerow((key, ideas_dict[key]))
            print "%i out of %i dates done" % (count, total)
            count += 1
combine()
