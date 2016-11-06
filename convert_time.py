from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import pandas as pd
import datetime

today_test = "Today, 5:54 PM"

yesterday_test = "Yesterday, 5:54 PM"

date_test = "Mon, Oct. 24, 5:04 PM"


def convert_time(time):
	if "Today" in time:
		pass
	else if "Yesterday" in time:
		pass
	else:
		pass

		