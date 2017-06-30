import scrapy
import pickle
import os
import re

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    with open('obj/' + name, 'rb') as f:
        return pickle.load(f)

class CommonFloor(scrapy.Spider):

    name = 'extract_html'

    def start_requests(self):
        for root, dirs, files in os.walk('obj/city_urls/'):
            for file in files:
                city = re.sub('urls_','',file)
                city = re.sub('.pkl','',city)
                if not os.path.exists('html/'+city):
                    os.makedirs('html/'+city)
                urls = load_obj('city_urls/'+file)
                for url in urls:
                    yield scrapy.Request(url=url,callback=self.parse,meta={'city':city})
            
    def parse(self, response):
        if response.status!= 200:
            file = 'html/%s/failed.txt' % response.meta['city']
            with open(file, 'a') as f:
                f.write(response.url)
                f.write("\n")

        project_id = re.split('/',response.url)[-1]
        project_id = re.sub('povp-','',project_id)
        file = 'html/%s/%s' % (response.meta['city'], project_id)
        with open(file, 'w') as f:
            f.write(response.body)
