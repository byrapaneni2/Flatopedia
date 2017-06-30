import scrapy
import pickle
import os
import json
import re

def load_obj(file):
    with open('obj/'+file+'.pkl') as f:
        return pickle.load(f)

def save_obj(obj, file):
    with open('obj/'+file+'.pkl', 'w') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

class CFListing(scrapy.Spider):

    name = "extract_html"

    def start_requests(self):
        base_url = "https://www.commonfloor.com/"

        cities = ['bangalore', 'delhi', 'gurgaon', 'noida', 'ghaziabad', 'greater noida', 'faridabad', 'hyderabad', 'pune', 'mumbai']
        for city in cities:
            if not os.path.exists('html/'+city):
                os.makedirs('html/'+city)

            end_urls = load_obj('city_urls/'+city)
            for end_url in end_urls:
                url = base_url + end_url
                yield scrapy.Request(url=url, callback=self.parse, meta = {'city':city})

    def parse(self, response):
        city = response.meta['city']
        id = re.split('/',response.url)[-1]

        with open('html/%s/%s'%(city,id), 'w') as f:
            f.write(response.body)
        





