import pandas as pd
import datetime
import csv

today_test = "Today, 5:54 PM"

yesterday_test = "Yesterday, 5:54 PM"

date_test = "Mon, Oct. 24, 5:04 PM"
date_test2 = "Apr. 20, 2015, 7:22 AM"




def convert_time(time):
    # print time
    months = {
        'Jan.': 1,
        'Feb.': 2,
        'Mar.': 3,
        'Apr.': 4,
        'May.': 5,
        'Jun.': 6,
        'Jul.': 7,
        'Aug.': 8,
        'Sep.': 9,
        'Oct.': 10,
        'Nov.': 11,
        'Dec.': 12,
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    try:
        time_array = time.split(', ')
        if "Today" in time_array[0]:
            out_time = datetime.date.today()
        elif "Yesterday" in time_array[0]:
            out_time = datetime.date.today() - datetime.timedelta(days=1)
        elif time_array[0][0:4] in months:
            year = int(time_array[1])
            date = time_array[0].split(' ')
            month = months[date[0]]
            day = int(date[1])
            out_time = datetime.date(year, month, day)
        elif time_array[0][0:3] in months:
            year = int(time_array[1])
            date = time_array[0].split(' ')
            month = months[date[0]]
            day = int(date[1])
            out_time = datetime.date(year, month, day)  
        else:
            year = 2016
            date = time_array[1].split(' ')
            month = months[date[0][0:4]]
            day = int(date[1])
            out_time = datetime.date(year, month, day)

        return out_time
    except IndexError:
        return None

