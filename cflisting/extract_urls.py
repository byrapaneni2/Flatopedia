import scrapy
import pickle
import json
import re
import os

def save_obj(obj, name):
	with open('obj/'+name+'.pkl','w') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
	with open('obj/'+name,'r') as f:
		return pickle.load(f)

urls = []
date = "Jun 20 2017"
cities = ['bangalore', 'delhi', 'gurgaon', 'noida', 'ghaziabad', 'greater noida', 'faridabad', 'hyderabad', 'pune', 'mumbai']

for city in cities:
	if not os.path.exists('obj/json_response/'+city):
		continue

	city_urls = []
	for file in os.listdir('obj/json_response/'+city):
		if not file.endswith('.pkl'):
			continue

		json_listings = load_obj('json_response/%s/%s'%(city,file))
		listings = json_listings["data"]
		count = 0
		group = 0
		projects = set()

		for listing_group in listings:
			if listing_group["card_type"] != "group":
				continue
			try:
				project_url = listing_group["project_data"]["project_url"]
			except KeyError:
				continue

			for listing in listing_group["children"]:
				if listing["posted_on"] != date:
					continue
				url = listing["posting_url"]
				urls.append(url)
				city_urls.append(url)

	save_obj(city_urls,'city_urls/'+city)
	print city, len(city_urls)

print len(urls)
