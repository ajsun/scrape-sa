from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import pandas as pd
import time

def main():
	base_url = "http://seekingalpha.com"
	long_ideas = "/stock-ideas/long-ideas"
	page = "?page="

	
	TIME_INDEX = 4

	article_ids = []
	article_titles = []
	article_links = []
	article_tickers = []
	article_times = []
	editors_picks = []
	article_bodys = []

	for i in range(1, 1439):
		if i is 1:
			r = requests.get(base_url + long_ideas, headers={'User-Agent': 'Mozilla/5.0'})
			print r.status_code
			r.raise_for_status()
			soup = BeautifulSoup(r.text, "lxml")
			article_list = soup.find(class_="articles-list").children
		else: 
			suffix = page + str(i)
			for x in range(0,5):
				try:
					r = requests.get(base_url + long_ideas + suffix, headers={'User-Agent': 'Mozilla/5.0'})
					print r.status_code
					r.raise_for_status()
					break
				except:
					continue
			if x == 4:
				raise Exception("GET failed")
			soup = BeautifulSoup(r.text, "lxml")
			article_list = soup.find(class_="articles-list").children
		
		for item in article_list:
			body = ""
			article_id = item.get('article_id')
			article_title = item.find(class_='media-body').a
			article_info = item.find(class_='a-info')

			editors_pick = False
			OFFSET = 4
			try: 
				if article_info.contents[0].string == "Editors' Pick":
					ticker = article_info.contents[OFFSET].get_text()
					article_time = article_info.contents[TIME_INDEX + OFFSET].contents[0]
					editors_pick = True
				else:
					ticker = article_info.contents[0].get_text()
					article_time = article_info.contents[TIME_INDEX].contents[0]
			except AttributeError as inst:
				print inst
				continue

			# try:
			# 	r = requests.get(base_url + article_title.get('href'), headers={'User-Agent': 'Mozilla/5.0'})
			# 	r.raise_for_status()
			# 	soup = BeautifulSoup(r.text, "lxml")
			# 	article_body = soup.find(id='main_content')
			# 	article_time = article_body.find('time').get('datetime')
			# 	body = article_body.get_text()
			# except Exception as inst:
			# 	print inst
			# 	print r.headers
			# 	time.sleep(5)
			# 	print "Sleeping for 5 seconds..."
			

			article_ids.append(article_id)
			article_titles.append(article_title.text)
			article_links.append(article_title.get('href'))
			article_tickers.append(ticker)
			article_times.append(article_time)
			editors_picks.append(editors_pick)
			article_bodys.append(body)

		print "Page %i is done" % (i)

		csv = { 'article_ids': article_ids,
				'article_titles': article_titles,
				'article_links': article_links,
				'article_tickers': article_tickers,
				'article_times': article_times,
				'editors_picks': editors_picks,
				'article_bodys': article_bodys}

		df = pd.DataFrame(csv)
		df.to_csv('long_ideas', index=False, mode='a', encoding='utf-8', columns=['article_ids', 
															  'article_tickers', 
															  'article_links',
															  'article_times',
															  'article_titles',
															  'editors_picks',
															  'article_bodys'])
		# print article_id
		# print article_body.get('href')
		# print article_body.contents[0]
		# print ticker
		# print time
		# print editors_pick
		# print '---------------------------\n'



# def pull_content(article_url):




if __name__ == "__main__":
	main()
	