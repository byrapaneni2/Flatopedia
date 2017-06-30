import scrapy
import json
import os
import pickle
import re

def load_obj(name):
    with open('obj/city_urls/' + name, 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open('obj/city_urls/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

class NinetyNineAcres(scrapy.Spider):
    
    name = "extract_html"
    
    def start_requests(self):
        for root, dirs, files in os.walk('obj/city_urls/'):
            for file in files:
                urls = load_obj(file)
                city = re.sub('.pkl', '', file)

                if not os.path.exists('html/'+city):
                    os.makedirs('html/'+city)
                
                for url in urls:
                    yield scrapy.Request(url=url,callback=self.parse,meta={'city':city})
            
    def parse(self, response):
        if response.status!= 200:
            file = 'html/%s/failed.txt' % response.meta['city']
            with open(file, 'a') as f:
                f.write(response.url)
                f.write("\n")

        project_id = response.xpath("//input[@id='npxidPROJ_ID']/@value").extract()
        if project_id:
            project_id = project_id[0]
            file = 'html/%s/%s' % (response.meta['city'], project_id)
            with open(file, 'w') as f:
                f.write(response.body)
        else:
            with open('log.txt', 'a') as f:
                f.write('No project_id in file ')
                f.write(response.url)
                f.write("\n")

