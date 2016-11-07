import pandas as pd
import numpy as np
import convert_time
import csv

with open('long_ideas.csv', 'r') as file:
    reader = csv.reader(file, delimiter = ',')
    header = True
    for row in reader:
        if header is True:
            header = False
            print "%s, %s, %s %s" % (row[0], row[1], row[2], row[3])
            continue

        article_id = row[0]
        stock_ticker = row[1]
        link = row[2]
        date = convert_time.convert_time(row[3])
        if date is None:
            continue
        print "%s, %s, %s, %s" % (article_id, stock_ticker, link, date)



