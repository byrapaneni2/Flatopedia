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

    name = "extract_listing_page"

    def start_requests(self):
        url = "https://www.commonfloor.com/nitro/search/search-results"
        params = {
            'search_intent': 'rent',
            'page': '',
            'city': '',
            'page_size': '20',
            'number_of_children': '10',
            'srtby': 'recency',
            'show_ungrouped_results': '0',
            'house_type': ["Apartment"]
        }
        # cities = load_obj('cities')
        cities = ['bangalore', 'delhi', 'gurgaon', 'noida', 'ghaziabad', 'greater noida', 'faridabad', 'hyderabad', 'pune', 'mumbai']
        for city in cities:
            if not os.path.exists('obj/json_response/'+city):
                os.makedirs('obj/json_response/'+city)
            if not os.path.exists('response/'+city):
            	os.makedirs('response/'+city)

            params['city'] = city
            for page in range(1,11):
                params['page'] = str(page)
                yield scrapy.Request(url=url, callback=self.parse, method="POST", body=json.dumps(params),
                                    meta = {'city':city, 'page':page}, dont_filter=True )

    def parse(self, response):
        city = response.meta['city']
        page = response.meta['page']

        text = response.text
        text = re.split("\n", text)[3]
        json_listings = json.loads(text)
        save_obj(json_listings, 'json_response/%s/%d'%(city,page))

        with open('response/%s/%d'%(city,page), 'w') as f:
            f.write(json.dumps(json_listings, indent=4, sort_keys=True))
        





